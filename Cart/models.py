from django.db import models
from django.contrib.auth.models import User
from Products.models import Product
from django.utils.translation import gettext as _

# Create your models here.


class Cart(models.Model):
    """Model definition for Cart."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem', verbose_name=_(""))

    class Meta:
        """Meta definition for Cart."""

        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        """Unicode representation of Cart."""
        return f"Cart for {self.user.username}"

    # def save(self):
    #     """Save method for Cart."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for Cart."""
    #     return ('')

    # TODO: Define custom methods here
    class CartItem(models.Model):
        """Model definition for CartItem."""

        # TODO: Define fields here
        cart = models.ForeignKey('Cart', verbose_name=_(""), on_delete=models.CASCADE)
        product = models.ForeignKey(
            Product, verbose_name=_(""), on_delete=models.CASCADE
        )
        quantity = models.PositiveIntegerField(_(""), default=1)

        class Meta:
            """Meta definition for CartItem."""

            verbose_name = "CartItem"
            verbose_name_plural = "CartItems"

        def __str__(self):
            """Unicode representation of CartItem."""
            return f"{self.quantity} * {self.product}"

        # def save(self):
        #     """Save method for CartItem."""
        #     pass

        # def get_absolute_url(self):
        #     """Return absolute url for CartItem."""
        #     return ""

        # TODO: Define custom methods here
