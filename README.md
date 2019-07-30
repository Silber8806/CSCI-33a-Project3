# Project 3

## Summary 

This is a restaurant application for a pizza and sub place.  Start by going to http://127.0.0.1:8000.

When you get into this website, you should first be prompted with a login page unless you are currently logged in.
On that login page, you can click the sign-up button to sign-up for the website.  If you have credentials, just use
them to login.

This will redirect you to the main page containing a menu.  Note the nav bar has changed.  You can click the left 
Menu button to go back to this menu page or on the right, you can click the "cart" or "orders" button to check out 
your current cart or see orders placed respectively.

Most likely at this point in time, you have no items in your cart and haven't placed an order.  In this case, you 
can press any item on the menu to go to a detailed product page with options.  All options are based on a base 
price plus a possible extra charge for things like: large size or more toppings.  Once you filled out the form
correctly, you can click the "add-to-cart" button to add it to your cart.  When you click this button you will
be redirected to the menu.  Note, the add-to-cart items have an "X" next to them, which you can click to delete 
an items from your cart.

Feel free to place a few different items into your cart using the above method.  Note that each product detail
page adjusts to the options provided by the administrator.  There are 3 types of information related to each 
product: product options, product variations and product categories.

* product categories -> represent broad categories on the menu like: pasta, subs and regular pizza.
* product variations -> currently only represent size (implemented), but could be extended in the future to include
other options.
* product options -> currently represents toppings, but could represent any group of options related to a product.

Once you have added all items you would like to purchase to cart, go to the top right corner cart button.  You
will notice that all added items are present including a total at the bottom right corner.  Feel free to press
checkout to complete your order.  Once completed, it will post the items to orderlineitems table and the bundle
representing all these products to the order table.

You can now go to the top right nav bar option: orders to see the current orders you have placed and their 
specific status (submitted, reviewed, delivered, fulfilled..etc).

Feel free to checkout the admin pannel at: 
http://127.0.0.1:8000/admin

As an admin you can add products, check orders and see the current state of the add-to-carts.

## Tables:

Feel free to use the below to check out table structures.  A quick explanation of each table:

* Product - Represents each product.
* ProductCategory -> Represents the product category and sort order of menu.
* ProductVariation -> Represents each product size (currently)
* ProductGroup -> Represents a list of options that a product could be associated with eg toppings.
* ProductGroupOptions -> actual options that can be associated with a ProductGroup -> Pizza => (pepperoni,olives)
* AddToCart -> Add-to-Cart events that have not been posted as an order.
* Order -> High-level instance involving a bundle of products that have been ordered.
* OrderLineItem -> Items ordered related to Orders table.

#### Indirectly referenced data models

The above represent tables from within orders app. Login and Sign-up utilize the Django built-in auth app and 
reference the User system directly.  No tables are "created" for this as they come pre-bundled with the auth
app.

```python
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
    ORDER_STATUS_CHOICES = (
        (1, 'submitted'),
        (2, 'reviewed'),
        (3, 'paid'),
        (4, 'delivering'),
        (5, 'fulfilled'),
    )
    user_fk = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    gross_amt = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

    def __str__(self):
        return f"{self.id} - {self.user_fk} - ${self.gross_amt} - {self.order_status} - {self.order_date.strftime('%m-%d-%Y %H:%M:%S')}"


class OrderLineItem(models.Model):
    order_fk = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    product_variations = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True)
    product_options = models.CharField(max_length=256, null=True)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    def line_total(self):
        return self.quantity * self.unit_price

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

```

##File Structure

The below is a directory structure of the entire application with some basic notes.

```
C:.
│   db.sqlite3 -> Database
│   manage.py -> Management utility
│   README.md -> This file
│   requirements.txt -> Dependencies
│
├───accounts -> Sign-up application
│   │   apps.py -> app file
│   │   forms.py -> only includes a sign-up form
│   │   urls.py -> sign-up urls
│   │   views.py -> sign-up view (function)
│   │   __init__.py
│
├───automation -> some automation
│   └───ddl
│           database.sql -> setting up basic database
│
├───orders
│   │   admin.py -> all the models are registered with admin here
│   │   apps.py -> orders app
│   │   models.py -> database models
│   │   urls.py -> most of the urls for the application...
│   │   views.py -> most of the views for the application
│   │   __init__.py
│   │
│   ├───migrations -> migrations for the ordres app
│   │
│   ├───static -> static file dir
│   │   ├───css -> all the css
│   │   │   │   styles.css -> The main styles.css used in the project
│   │   │   │   styles.css.map
│   │   │   │   styles.scss -> Sass file containing the ocde I used
│   │   │
│   │   ├───images
│   │   │       logo.gif -> Actual logo off pinnochio's website (saved and downloaded)
│   │   │
│   │   └───js
│   │           cart.js -> JavaScript used only on Cart page, does AJAX Post request to delete items.
│   │           product.js -> JavaScript used to do calculations/submissions on the product page.
│
├───pizza
│   │   settings.py -> settings for the project.
│   │   urls.py -> central url file
│   │   wsgi.py -> wsgi file
│   │   __init__.py
│
└───templates
    ├───accounts -> templates for accounts app
    │       signup.html -> only template is the sign-up template
    │
    ├───orders
    │       cart.html -> This is the virtual cart page used to view what is currently in your cart.
    │       index.html -> main website page featuring the menu
    │       orders.html -> page for orders that have been placed viewable by each user (for each user)
    │       product.html -> page for a single product.
    │
    ├───registration
    │       login.html -> login page
    │
    └───templates
            base.html -> template for the rest of the site.
```

## Notes:

cart.js -> I had a hardtime implementing CSRF tokens over AJAX post requests and ended up using the one provided
on the django website that uses JQuery.  I ended up switching out JQuery slim minimized for JQuery minimized to
support this functionality.  It's the only use of JQuery within the project outside of bootstrap.

orders -> view.py -> checkout function -> this uses a transaction within the function instead of relying on
the auto-commit feature of Django.  I didn't want to post an order unless both orderlineitem and order are committed
at the same time.  If either fails, it should rollback to the previous state and error out instead.  I ended up
using the transaction instead of transaction decorator as I wasn't sure if I was going to add more logic to 
that specific function.  I wish I had more time to test this out.

## Improvements

Admin needs a ton of improvements and I didn't have enough time to do it:
* Product Category should show the sort order on the admin page.
* Product Variation should use absolute price instead of value added.
* Product Variation would probably best be served if product had a default size (small), but I built it to be 
too general.  I thought more than size would show up.  I ended up only implementing size, which you can 
see in the orders page (I pass only the size parameter instead of all possible sizes).
* I wish I had used some of the more advanced admin features to create list views for product etc or show 
product variations and product options when you click a product.
*  There is no default UI sort order, which is a huge problem in terms of updating information.  Wish I had
at least created some kind of dynamic sorting.

Testing:
* This entire project could use through testing.  Especially since we are dealing with monetary transactions.  Luckily
this project isn't live.

CSS:
* I wish I had time to do a bit more re-org in this department.

JS: 
* I ended up using JQuery for the AJAX post request for deleting items.  I wish I figured out how to use 
vanilla javascript, but just didn't have time for it.

## Sources:

All pricing and products are based on Pinocchio's website presented within the class.  I used the logo from the 
website within this project as well.  You can find this information at:

http://pinocchiospizza.net/menu.html

