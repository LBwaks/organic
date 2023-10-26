from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
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

# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "category").prefetch_related("tag")
        return queryset


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
