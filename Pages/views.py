from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from Products.models import Product, Category, Tag

# Create your views here.


class Home(ListView):
    model = Product
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.select_related("user")
        tag_by_category = Tag.objects.select_related("user", "category").filter(
            category=category
        )
        context = {"categories": categories}
        return context


class About(TemplateView):
    template_name = "pages/about-us.html"
