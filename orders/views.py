from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse

from .models import Product

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