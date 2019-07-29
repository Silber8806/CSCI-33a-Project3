from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:product_id>",views.product_info,name="product"),
    path("addtocart/",views.addtocart,name="addtocart"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("removefromcart/",views.removefromcart,name="removefromcart"),
    path("orders/",views.orders,name="order"),
]
