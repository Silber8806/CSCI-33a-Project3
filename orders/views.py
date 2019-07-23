from django.http import HttpResponse
from django.shortcuts import render

from .models import Product

# Create your views here.
def index(request):
    context = {
        "products": Product.objects.select_related('product_category_fk').order_by(
                'product_category_fk__sort_order',
                'product_name',
                )
    }
    return render(request,'orders/index.html',context)
