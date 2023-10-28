from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductByCategoryListView,
    ProductByTagListView,
    ProductByUserListView,
    ProductFilterView,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="products"),
    path("product-details/<slug>", ProductDetailView.as_view(), name="product-details"),
    path("add-product/", ProductCreateView.as_view(), name="add-product"),
    path("update-product/<slug>", ProductUpdateView.as_view(), name="update-product"),
    path("delete-product/<slug>", ProductDeleteView.as_view(), name="delete-product"),
    path(
        "user-product/<username>", ProductByUserListView.as_view(), name="user-product"
    ),
    path(
        "category-product/<slug>",
        ProductByCategoryListView.as_view(),
        name="category-product",
    ),
    path("tag-product/<slug>", ProductByTagListView.as_view(), name="tag-product"),
    path("product-filter/", ProductFilterView.as_view(), name="product-filter"),
]
