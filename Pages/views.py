from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from Products.models import Product, Category, Tag
from Pages.forms import ContactForm, ProductSearchForm
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.


def product_search(request):
    form = ProductSearchForm
    results = None
    if request.method == "GET":
        if "q" in request.GET:
            form = ProductSearchForm(request.GET)
            if form.is_valid():
                q = form.cleaned_data["q"]
                print(q)
                search_query = SearchQuery(q)
                search_vector = (
                    SearchVector("title")
                    + SearchVector("category__name", weight="B")
                    # + SearchVector("tag", weight="B")
                    # + SearchVector("description", weight="A")
                )
                search_rank = SearchRank(search_vector, search_query)
                results = Product.objects.annotate(
                    search=search_vector, rank=search_rank
                ).order_by("-rank")

    return render(
        request, "pages/search.html", {"form": form, "results": results, "q": q}
    )


class Home(ListView):
    model = Product
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.select_related("user")
        cat_tag_dict = {}
        for category in categories:
            tags = Tag.objects.select_related("user", "category").filter(
                category=category
            )
            cat_tag_dict[category] = tags

        context = {"cat_tag_dict": cat_tag_dict}
        return context


class About(TemplateView):
    template_name = "pages/about-us.html"


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            from_email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            tell = form.cleaned_data["tell"]
            message = form.cleaned_data["message"]
            try:
                send_mail(subject, message, from_email, ["lovubi1@gmail.com"])
            except BadHeaderError:
                return HttpResponse("Invalid Header Found!")
            return HttpResponseRedirect("home")
    else:
        form = ContactForm()
    return render(request, "pages/contact-us.html", {"form": form})
