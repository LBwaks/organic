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
from .filters import ProductFilter
from django_filters.views import FilterView
from django.core.paginator import Paginator

# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "category").prefetch_related("tag")
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # get categories
        categories = Category.objects.select_related("user")
        context["categories"] = categories
        # product filter
        context["filter"] = ProductFilter(
            self.request.GET, queryset=self.get_queryset()
        )
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


class ProductFilterView(FilterView):
    model = Product
    template_name = "products/product-filter.html"
    filterset_class = ProductFilter
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        product_filter = ProductFilter(request.GET, queryset=self.get_queryset())
        paginator = Paginator(product_filter.qs, self.paginate_by)
        page_number = request.GET.get("page")
        products = paginator.get_page(page_number)

        categories = Category.objects.select_related("user")
        return render(
            request,
            self.template_name,
            {
                "products": products,
                "categories": categories,
                "product_filter": product_filter,
            },
        )

    def get_queryset(self):
        queryset = Product.objects.select_related("user", "category").prefetch_related(
            "tag"
        )
        product_filter = ProductFilter(self.request.GET, queryset=queryset)

        return product_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_filter"] = ProductFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context
