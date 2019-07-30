from django.contrib import admin

# customer tables
from .models import (
    Product,
    ProductCategory,
    ProductVariation,
    ProductGroup,
    ProductGroupOption,
    Order,
    OrderLineItem,
    AddToCart
)

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductGroup)
admin.site.register(ProductGroupOption)
admin.site.register(Order)
admin.site.register(ProductVariation)
admin.site.register(OrderLineItem)
admin.site.register(AddToCart)
