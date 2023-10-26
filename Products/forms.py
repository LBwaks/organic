from django import forms
from .models import Product, Tag, ProductImage
from ckeditor.widgets import CKEditorWidget


class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = ("title", "category", "tag", "description", "price", "quantity")
        wigdets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            # "tag",
            "description": CKEditorWidget(),
            "price": forms.IntegerField(),
            "quantity": forms.TextInput(attrs={"class": "form-control"}),
        }


class EditProductForm(forms.ModelForm):
    """Form definition for Product."""

    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = ("title", "category", "tag", "description", "price", "quantity")
        wigdets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            # "tag",
            "description": CKEditorWidget(),
            "price": forms.IntegerField(),
            "quantity": forms.TextInput(attrs={"class": "form-control"}),
        }
