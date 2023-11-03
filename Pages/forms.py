from django import forms
from Pages.models import Contact
from phonenumber_field.formfields import PhoneNumberField


class ContactForm(forms.ModelForm):
    """Form definition for Contact."""

    # tell = PhoneNumberField(region="KE")

    class Meta:
        """Meta definition for Contactform."""

        model = Contact
        fields = ("name", "email", "subject", "message")

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control name" "required"}),
            "email": forms.EmailInput(attrs={"class": "form-control email" "required"}),
            "message": forms.Textarea(
                attrs={"class": "form-control message" "required"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control subject" "required"}
            ),
        }
