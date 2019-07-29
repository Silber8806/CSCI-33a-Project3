from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ProductGroup(models.Model):
    group_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.group_name}"


class ProductGroupOption(models.Model):
    option_name = models.CharField(max_length=64)
    option_unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    group_fk = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.option_name} - $ {self.option_unit_price}"


class ProductCategory(models.Model):
    product_category_name = models.CharField(max_length=64)
    sort_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_category_name}"


class Product(models.Model):
    product_name = models.CharField(max_length=64)
    product_category_fk = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING)
    product_group_fk = models.ForeignKey(ProductGroup, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    option_num_min = models.IntegerField(default=0)
    option_num_max = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product_name} - {self.product_category_fk.product_category_name}- $ {self.product_unit_price}"


class ProductVariation(models.Model):
    variation_name = models.CharField(max_length=64)
    variation_category = models.CharField(max_length=64)
    variation_unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_fk.product_name} - {self.variation_name} - $ {self.variation_unit_price + self.product_fk.product_unit_price}"


class Order(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_status = models.CharField(max_length=64)
    gross_amt = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

    def __str__(self):
        return f"{self.id} - {self.user_fk} - ${self.gross_amt} - {self.order_date.strftime('%m-%d-%Y %H:%M:%S')}"


class OrderLineItem(models.Model):
    order_fk = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    product_variations = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True)
    product_options = models.CharField(max_length=256, null=True)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order_fk.id} - {self.order_fk.user_fk} - {self.product_fk.product_name} - ${self.unit_price} - {self.quantity}"


class AddToCart(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variation_fk = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True)
    product_options = models.CharField(max_length=256, null=True)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    order_line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"This is a order..."
