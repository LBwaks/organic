from .models import Cart


def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.get(session_id=request.session.get("guest"))
    cart_items = cart.cartitems.all()
    return {"cart_items": cart_items, "cart": cart}
