from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Category, Tag, Product, ProductImage
from .forms import ProductForm, EditProductForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify

# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "category").prefetch_related("tag")
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories = Category.objects.select_related("user")
        context["categories"] = categories
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = "products/add-product.html"
    form_class = ProductForm

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        images = self.request.FILES.getlist("images")
        for image in images:
            ProductImage.objects.create(product=p, image=image)
            print(image)
        p.save()

        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products/update-product.html"
    form_class = EditProductForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.user != self.request.user:
            messages.error(request, "You do not have permission to edit this product.")
            return redirect(reverse("product-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        p = form.save(commit=False)
        images = self.request.FILES.getlist("images")
        for image in images:
            ProductImage.objects.update(image=image)
        p.save_m2m()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/delete-product.html"
    success_url = reverse_lazy("products")
    success_message = "Product Deleted"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.user != self.request.user:
            messages.error(
                request, "You do not have permission to delete this product."
            )
            return redirect(reverse("product-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ProductByCategoryListView(ListView):
    model = Product
    template_name = "products/product-category.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related("category", "user")
            .prefetch_related("tag")
        )
        products = queryset.filter(category=self.category)

        return products


class ProductByTagListView(ListView):
    model = Product
    template_name = "products/product-tag.html"
    context_object_name = "products"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related("category", "user")
            .prefetch_related("tag")
        )
        products = queryset.filter(tag=self.tag)

        return products


class ProductByUserListView(ListView):
    model = Product
    template_name = "products/product-user.html"
    context_object_name = "products"

    def get_queryset(self):
        self.username = self.kwargs.get("username")  # get username
        slugified_username = slugify(self.username)  # convert username to slug
        user = User.objects.filter(username=slugified_username).first()
        queryset = super().get_queryset()
        if not user:
            return Product.objects.none()
        products = (
            queryset.filter(user=user)
            .order_by("-created")
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tag")
        )
        return products
