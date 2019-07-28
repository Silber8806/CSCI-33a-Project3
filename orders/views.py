from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, ProductVariation, ProductGroup, ProductGroupOption

# Create your views here.
def index(request):
    context = {
        "products": Product.objects.select_related('product_category_fk').order_by(
                'product_category_fk__sort_order',
                'product_unit_price',
                'product_name'
                )
    }
    return render(request,'orders/index.html',context)

def product_info(request, product_id):
    product_options=ProductGroupOption.objects.filter(
        group_fk=Product.objects.filter(pk=product_id).values('product_group_fk')[0]['product_group_fk'])\
        .values('id','option_name','option_unit_price')\
        .order_by('option_name')
    context = {
        "product": Product.objects.get(pk=product_id),
        "variations": list(
            ProductVariation.objects.filter(product_fk_id=product_id)
                .values('id','variation_name','variation_category','variation_unit_price')
                .order_by('-variation_name')
        ),
        "options": list(product_options)
    }
    return render(request, 'orders/product.html', context)

def addtocart(request):
    return redirect('index');