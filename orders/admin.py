from django.contrib import admin

# customer tables
from .models import (
    Customer,
    Address,
    Product,
    ProductCategory,
    ProductVariation,
    ProductGroup,
    ProductGroupOption,
    Order,
    OrderLineItem
)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductVariation)
admin.site.register(ProductGroup)
admin.site.register(ProductGroupOption)
admin.site.register(Order)
admin.site.register(OrderLineItem)