from django.shortcuts import get_object_or_404, redirect, render
from Cart.models import CartItem, Cart
from Products.models import Product
from django.views.generic import ListView, View

# Create your views here.


# class CartListView(ListView):
#     model = Cart

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(user=self.request.user)
#         # queryset = CartItem.objects.filter(cart= queryset)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_cart = self.get_queryset().first()
#         # cart = Cart.objects.filter(user=self.request.user)
#         cart_items = CartItem.objects.filter(cart=user_cart)
#         context["cart_items"] = cart_items
#         return context

#     template_name = "carts/carts.html"


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitems.all()
    return render(request, "carts/carts.html", {"cart_items": cart_items, "cart": cart})


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("products")
