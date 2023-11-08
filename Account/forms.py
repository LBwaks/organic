from django import forms
from .models import Profile, Shipping
from phonenumber_field.formfields import PhoneNumberField


class ProfileForm(forms.ModelForm):
    """Form definition for Profile."""

    #
    class Meta:
        """Meta definition for Profileform."""

        tell = PhoneNumberField(region="KE")
        model = Profile
        fields = ("fname", "lname", "email", "tell", "profile")

        widgets = {
            "fname": forms.TextInput(
                attrs={"class": "form-control fname ", "required": True}
            ),
            "lname": forms.TextInput(
                attrs={"class": "form-control lname", "required": True}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control email", "required": True}
            ),
            # "tell",
            "profile": forms.ClearableFileInput(
                attrs={"class": "form-control profile"}
            ),
        }


class ShippingForm(forms.ModelForm):
    """Form definition for Shipping."""

    class Meta:
        """Meta definition for Shippingform."""

        tell = PhoneNumberField(region="KE")

        model = Shipping
        fields = (
            "fname",
            "lname",
            "tell",
            "email",
            "country",
            "region",
            "city",
            "street",
            "more_street",
        )
        widget = {
            "fname": forms.TextInput(
                attrs={"class": "form-control fname ", "required": True}
            ),
            "lname": forms.TextInput(
                attrs={"class": "form-control lname", "required": True}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control email", "required": True}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control country ", "required": True}
            ),
            "region": forms.TextInput(
                attrs={"class": "form-control region", "required": True}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control city ", "required": True}
            ),
            "street": forms.TextInput(
                attrs={"class": "form-control street", "required": True}
            ),
            "more_street": forms.Textarea(
                attrs={"class": "form-control more_street", "required": True}
            ),
        }
