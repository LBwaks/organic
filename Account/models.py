from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    slug = models.UUIDField(editable=False, default=uuid.uuid4)
    fname = models.CharField(_("First Name"), max_length=50)
    lname = models.CharField(_("Last Name"), max_length=50)
    email = models.EmailField(_("Email"), unique=True, max_length=254)
    tell = PhoneNumberField(_("Tell"))
    profile = models.ImageField(
        _("Profile"),
        upload_to="profiles/",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        
    )
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """Unicode representation of Profile."""
        return f'{self.fname} {self.lname}'

    # def save(self):
    #     """Save method for Profile."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Profile."""
        return ""

    # TODO: Define custom methods here


class Shipping(models.Model):
    """Model definition for Shipping."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    fname = models.CharField(_("First Name"), max_length=50)
    lname = models.CharField(_("Last Name"), max_length=50)
    slug = models.UUIDField(editable=False, default=uuid.uuid4)
    tell = PhoneNumberField(_("Phone Number"))
    email = models.EmailField(_("Email"), max_length=254)
    country = models.CharField(_("Country"), default="Kenya", max_length=50)
    region = models.CharField(_("Region"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    street = models.CharField(_("Street"), max_length=50)
    more_street = models.TextField(_("Addition Street Information"))
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Shipping."""

        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        """Unicode representation of Shipping."""
        return f'{self.fname} {self.lname}'

    # def save(self):
    #     """Save method for Shipping."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Shipping."""
        return ""

    # TODO: Define custom methods here


class Billing(models.Model):
    """Model definition for Billing."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    fname = models.CharField(_("First Name"), max_length=50)
    lname = models.CharField(_("Last Name"), max_length=50)
    slug = models.UUIDField(editable=False, default=uuid.uuid4)
    email = models.CharField(_("Email"), max_length=50)
    tell = PhoneNumberField(_("Phone Number"))
    status = models.CharField(_(""),default='pending', max_length=50)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Billing."""

        verbose_name = "Billing"
        verbose_name_plural = "Billings"

    def __str__(self):
        """Unicode representation of Billing."""
        return f'{self.fname} {self.lname}'

    # def save(self):
    #     """Save method for Billing."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Billing."""
        return ""

    # TODO: Define custom methods here
