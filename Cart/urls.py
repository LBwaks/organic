from django.urls import path
from .views import add_to_cart, cart, remove_cart_item, delete_cart, checkout

urlpatterns = [
    path("cart/", cart, name="cart"),
    path("add-to-cart/<slug>", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>", remove_cart_item, name="remove-from-cart"),
    path("delete-cart/<slug>", delete_cart, name="delete-cart"),
    path("checkout", checkout, name="checkout"),
]
