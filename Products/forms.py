from django import forms
from .models import Product, Tag, ProductImage, Rating
from ckeditor.widgets import CKEditorWidget


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(
    #         attrs={"class": "form-control image", "required": True}
    #     ),
    # )
    images = MultipleFileField()
    tag = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={"class": "form-select tags", "required": True, "id": "product-id"}
        ),
        queryset=Tag.objects.all(),
    )

    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = (
            "title",
            "category",
            "tag",
            "unit",
            "price",
            "quantity",
            "description",
        )
        wigdets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "eg , Nyandarua Carrots",
                    "class": "form-control title",
                    "required": True,
                }
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
        fields = (
            "title",
            "unit",
            "category",
            "tag",
            "description",
            "price",
            "quantity",
        )
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


class RatingForm(forms.ModelForm):
    """Form definition for Rating."""

    class Meta:
        """Meta definition for Ratingform."""

        model = Rating
        fields = ("title", "ratings", "review")

        widget = {
            "title": forms.TextInput(
                attrs={"class": "form-control title", "required": True}
            ),
            "ratings": forms.Select(
                attrs={"class": "form-select ratings", "required": True}
            ),
            "review": forms.Textarea(
                attrs={"class": "form-control quantity", "required": True}
            ),
        }
