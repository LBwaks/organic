from typing import Any
from django.contrib import admin
from .models import Category, Tag, Product, ProductImage


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin View for Category"""

    list_display = ("name", "description", "is_published", "is_featured", "created")
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ("user",)

    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin View for Tag"""

    list_display = ("name", "description", "is_published", "is_featured", "created")
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ("user",)

    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin View for Product"""

    list_display = ("product_reference", "title", "category", "price", "quantity")
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ("user",)
    # search_fields = ('',)
    # date_hierarchy = ''
    ordering = ("-created",)

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
