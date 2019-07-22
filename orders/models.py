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

class ProductVariation(models.Model):
    variation_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.variation_name}"

class ProductVariationOption(models.Model):
    product_option_name = models.CharField(max_length=64)
    product_option_unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    variation_fk = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_option_name} - $ {self.product_option_unit_price}"

class ProductType(models.Model):
    product_type_name = models.CharField(max_length=64, blank=True)
    sort_order = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.product_type_name}"

class Product(models.Model):
    NONE = 'N'
    SMALL = 'S'
    LARGE = 'L'
    SIZE_CHOICES = [
        (NONE, None),
        (SMALL, 'Small'),
        (LARGE, 'large'),
    ]
    product_name = models.CharField(max_length=64,blank=True)
    product_type = models.CharField(max_length=64, blank=True)
    product_type_fk = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_variation_fk = models.ForeignKey(ProductVariation, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_size = models.CharField(
        max_length=1,
        choices=SIZE_CHOICES,
        default=SMALL,
        blank=False,
        null=True
    )
    product_options_limit = models.IntegerField()
    product_unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product_type} - {self.product_size} - {self.product_name} - $ {self.product_unit_price}"

class Order(models.Model):
    customer_fk = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="customer")
    address_fk = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="address")
    order_status = models.CharField(max_length=64)
    gross_amt = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amt = models.DecimalField(max_digits=12, decimal_places=2)
    total_amt = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateTimeField()

    def __str__(self):
        return f"This is a order..."


class OrderLineItem(models.Model):
    order_fk = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    product_fk = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="product")
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"This is a order..."
