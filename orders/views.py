from django.http import HttpResponse
from django.shortcuts import render

from .models import Product

# Create your views here.
def index(request):
    context = {
        "products": Product.objects.select_related('product_type_fk').order_by(
                'product_type_fk__sort_order',
                'product_type_fk__product_type_name',
                'product_name',
                'product_size'
                )
    }
    return render(request,'orders/index.html',context)
