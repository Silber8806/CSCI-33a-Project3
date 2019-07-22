from django.contrib import admin

# customer tables
from .models import (
    Customer,
    Address,
    Product,
    ProductType,
    ProductVariation,
    ProductVariationOption,
    Order,
    OrderLineItem
)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductVariation)
admin.site.register(ProductVariationOption)
admin.site.register(Order)
admin.site.register(OrderLineItem)