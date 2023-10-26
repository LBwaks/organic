from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="products"),
    path("product-details/<slug>", ProductDetailView.as_view(), name="product-details"),
    path("add-product/", ProductCreateView.as_view(), name="add-product"),
    path("update-product/<slug>", ProductUpdateView.as_view(), name="update-product"),
    path("delete-product/<slug>", ProductDeleteView.as_view(), name="delete-product")
]
