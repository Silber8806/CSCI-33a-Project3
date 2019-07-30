from django.shortcuts import render, redirect, get_object_or_404

import json

from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import AddToCart, Product, ProductVariation, ProductGroupOption, Order, OrderLineItem


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    context = {
        "products": Product.objects.select_related('product_category_fk').order_by(
            'product_category_fk__sort_order',
            'product_unit_price',
            'product_name'
        )
    }
    return render(request, 'orders/index.html', context)


@login_required(login_url='/accounts/login/')
def product_info(request, product_id):
    get_object_or_404(Product, pk=product_id)
    product_options = ProductGroupOption.objects.filter(
        group_fk=Product.objects.filter(pk=product_id).values('product_group_fk')[0]['product_group_fk']) \
        .values('id', 'option_name', 'option_unit_price') \
        .order_by('option_name')
    context = {
        "product": Product.objects.get(pk=product_id),
        "variations": list(
            ProductVariation.objects.filter(product_fk_id=product_id)
                .values('id', 'variation_name', 'variation_category', 'variation_unit_price')
                .order_by('-variation_name')
        ),
        "options": list(product_options)
    }
    return render(request, 'orders/product.html', context)


@login_required(login_url='/accounts/login/')
def addtocart(request):
    try:
        product_variant = ProductVariation.objects.get(id=int(request.POST.get('size', 0)))
    except ProductVariation.DoesNotExist:
        product_variant = None

    product_options = request.POST.getlist('options')
    if (len(product_options) > 0):
        product_options = ', '.join(product_options)
    else:
        product_options = None

    new_cart_item = AddToCart(user_fk=User.objects.get(id=int(request.POST['user'])),
                              product_fk=Product.objects.get(pk=int(request.POST['product_id'])),
                              product_variation_fk=product_variant,
                              product_options=product_options,
                              unit_price=request.POST['per-unit-price'],
                              quantity=request.POST['quantity'],
                              order_line_total=request.POST['order-total']
                              )
    new_cart_item.save()
    return redirect('index');


@login_required(login_url='/accounts/login/')
def cart(request):
    items = AddToCart.objects.filter(user_fk=request.user.id) \
        .select_related('product_fk', 'product_variation_fk', 'product_fk__product_category_fk') \
        .values('id',
                'product_fk__product_name',
                'product_fk__product_category_fk__product_category_name',
                'product_variation_fk__variation_name',
                'product_options',
                'unit_price',
                'quantity',
                'order_line_total') \
        .order_by('product_fk__product_name')

    context = {
        "items": items
    }
    return render(request, 'orders/cart.html', context)


@login_required(login_url='/accounts/login/')
def removefromcart(request):
    if request.method == 'DELETE':
        item = QueryDict(request.body).get('item')
        AddToCart.objects.get(pk=item).delete();

    return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
        content_type="application/json"
    )


@login_required(login_url='/accounts/login/')
def checkout(request):
    with transaction.atomic():
        new_order = Order(user_fk=request.user,
                          order_status=1,
                          gross_amt=request.POST.get('total-checkout', 0.00))

        current_cart_items = AddToCart.objects.filter(user_fk=request.user.id) \
            .values('id',
                    'product_fk',
                    'product_variation_fk',
                    'product_options',
                    'unit_price',
                    'quantity')

        new_order.save()

        for item in current_cart_items:
            new_order_line_item = OrderLineItem(order_fk=new_order,
                                                product_fk=Product.objects.get(pk=int(item['product_fk'])),
                                                product_variations=ProductVariation.objects.get(
                                                    pk=int(item['product_variation_fk'])) if item[
                                                    'product_variation_fk'] else None,
                                                product_options=item['product_options'],
                                                unit_price=item['unit_price'],
                                                quantity=item['quantity']
                                                )
            new_order_line_item.save()
            AddToCart.objects.get(pk=int(item['id'])).delete()
    return redirect('index')


@login_required(login_url='/accounts/login/')
def orders(request):
    orderlineitems = OrderLineItem.objects.filter(order_fk__user_fk=request.user.id) \
        .select_related('order_fk') \
        .order_by('order_fk__order_date',
                  'product_fk__product_name')
    context = {
        "orders": orderlineitems
    }
    return render(request, 'orders/orders.html', context)
