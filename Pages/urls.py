from django.urls import path
from .views import Home, contact

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("contact-us/", contact, name="contact"),
]
