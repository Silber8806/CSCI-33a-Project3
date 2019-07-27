from django.db import models


# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.IntegerField()

    def __str__(self):
        return f"This is a order..."


class Address(models.Model):
    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip_code = models.IntegerField()

    def __str__(self):
        return f"This is a order..."


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
    product_group_fk = models.ForeignKey(ProductGroup, on_delete=models.DO_NOTHING, null=True,blank=True)
    product_unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    option_num_min = models.IntegerField(default=0)
    option_num_max = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product_name} - { self.product_category_fk.product_category_name}- $ {self.product_unit_price}"


class ProductVariation(models.Model):
    variation_name = models.CharField(max_length=64)
    variation_category = models.CharField(max_length=64)
    variation_unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_fk.product_name} - {self.variation_name} - $ {self.variation_unit_price + self.product_fk.product_unit_price}"


class Order(models.Model):
    customer_fk = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    address_fk = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    order_status = models.CharField(max_length=64)
    gross_amt = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amt = models.DecimalField(max_digits=12, decimal_places=2)
    total_amt = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateTimeField()

    def __str__(self):
        return f"This is a order..."


class OrderLineItem(models.Model):
    order_fk = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"This is a order..."
