from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
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
        p.save()
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products/update-product.html"
    form_class = EditProductForm


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/delete-product.html"
    success_url = reverse_lazy('products')
