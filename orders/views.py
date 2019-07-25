from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

def product_info(request):
    product_id=1
    product_data = {
        "products": list(ProductVariation.objects.filter(product_fk_id = product_id).values()),
        "options": list(Product.objects.filter(id = product_id).select_related('product_group_fk_id').values())
    }
    return JsonResponse(product_data, safe=False)