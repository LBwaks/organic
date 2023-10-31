from django.urls import path
from .views import add_to_cart, cart

urlpatterns = [
    path("cart/", cart, name="cart"),
    path("add-to-cart/<slug>", add_to_cart, name="add-to-cart"),
]
