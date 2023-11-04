from django.urls import path
from .views import Home, contact, product_search

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("contact-us/", contact, name="contact"),
    path("search", product_search, name="search"),
]
