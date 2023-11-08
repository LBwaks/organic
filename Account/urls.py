from django.urls import path
from .views import ProfileUpdateView, UserProfile,ShippingCreateView

urlpatterns = [
    path("profile/<slug>", UserProfile.as_view(), name="profile"),
    path("change/<slug>", ProfileUpdateView.as_view(), name="change"),
    path("add-shipping/", ShippingCreateView.as_view(), name="add-shipping")
]
