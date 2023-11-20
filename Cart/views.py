import uuid
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
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.get(session_id=request.session.get("guest"))
    cart_items = cart.cartitems.all()
    return render(request, "carts/carts.html", {"cart_items": cart_items, "cart": cart})


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        # If the user is authenticated, use their user-based cart
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # If the user is not authenticated, use a session-based cart
        session_id = request.session.get("guest")
        if not session_id:
            # Generate a new session ID if it doesn't exist
            session_id = str(uuid.uuid4())
            request.session["guest"] = session_id

        cart, created = Cart.objects.get_or_create(session_id=session_id)

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        # If the product is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# return HttpResponse("Added")


def add_item(request):
    return redirect()


def remove_cart_item(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(
            session_id=request.session.get(
                "guest",
            )
        )
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

    except CartItem.DoesNotExist:
        return redirect("cart")

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")


def delete_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(
            session_id=request.session.get(
                "guest",
            )
        )
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

    except CartItem.DoesNotExist:
        return redirect("cart")

    cart_item.delete()
    return redirect("cart")


def checkout(request):
    return render(request, "carts/checkout.html")
