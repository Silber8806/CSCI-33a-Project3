from django.db import models

# Create your models here.

class Order(models.Model):
    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    address_fk = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address")
    order_status = models.CharField(max_length=64)
    gross_amt = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amt = models.DecimalField(max_digits=12, decimal_places=2)
    total_amt = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f("This is a order...")


class OrderLineItems(models.Model):
    order__fk = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f("This is a order...")


class Product(models.Model):
    product_description = models.CharField(max_length=64)
    product_size = models.CharField(max_length=32)
    product_options_limit = models.IntegerField()
    product_unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f("This is a order...")


class ProductOptions(models.Model):
    product_option_description = models.CharField(max_length=64)
    product_option_unit_price = models.DecimalField(map_digits=5, decimal_places=2)
    product_id_fk = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="production_options")

    def __str__(self):
        return f("This is a order...")


class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = PhoneNumberField()

    def __str__(self):
        return f("This is a order...")


class Address(models.Model):
    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    street = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip_code = models.IntegerField()

    def __str__(self):
        return f("This is a order...")