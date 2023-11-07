from django.forms import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """Form definition for Profile."""

    class Meta:
        """Meta definition for Profileform."""

        model = Profile
        fields = ("fname", "lname", "email", "tell", "profile")

        widgets = {
            "fname": forms.TextInput(
                attrs={"class": "form-control fname ", "required": True}
            ),
            # "lname", "email", "tell", "profile"
        }
