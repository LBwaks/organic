from django import forms
from .models import Product, Tag, ProductImage
from ckeditor.widgets import CKEditorWidget


class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    images = forms.ImageField(
        
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control image", "required": True}
        ),
    )
    tag = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={"class": "form-select tags", "required": True, "id": "product-id"}
        ),
        queryset=Tag.objects.all(),
    )

    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = ("title",'unit', "category",'tag',  "description", "price", "quantity")
        wigdets = {
            "title": forms.TextInput(
                attrs={"class": "form-control title", "required": True}
            ),
            "unit": forms.TextInput(
                attrs={"class": "form-control unit", "required": True}
            ),
            "category": forms.Select(
                attrs={"class": "form-select category", "required": True}
            ),
            # "tag",
            "description": CKEditorWidget(attrs={"required": True}),
            "price": forms.TextInput(
                attrs={"class": "form-control price", "required": True}
            ),
            "quantity": forms.TextInput(
                attrs={"class": "form-control quantity", "required": True}
            ),
        }


class EditProductForm(forms.ModelForm):
    """Form definition for Product."""

    images = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control image", "required": True}
        ),
    )
    tag = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={"class": "form-select tags", "required": True, "id": "product-id"}
        ),
        queryset=Tag.objects.all(),
    )

    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = ("title", 'unit',"category",'tag', "description", "price", "quantity")
        wigdets = {
            "title": forms.TextInput(
                attrs={"class": "form-control title", "required": True}
            ),
            "unit": forms.TextInput(
                attrs={"class": "form-control unit", "required": True}
            ),
            "category": forms.Select(
                attrs={"class": "form-select category", "required": True}
            ),
            # "tag",
            "description": CKEditorWidget(attrs={"required": True}),
            "price": forms.TextInput(
                attrs={"class": "form-control price", "required": True}
            ),
            "quantity": forms.TextInput(
                attrs={"class": "form-control quantity", "required": True}
            ),
        }
