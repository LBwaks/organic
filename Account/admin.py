# from typing import Any
from typing import Any
from django.contrib import admin
from .models import Profile, Shipping


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin View for Profile"""

    list_display = ("fname", "lname", "email", "created")
    # list_filter = ("",)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ("",)
    readonly_fields = ("user",)
    search_fields = ("fname", "lname", "email", "created")

    # date_hierarchy = ""
    # ordering = ("",)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    """Admin View for Shipping"""

    list_display = ("fname", "lname", "tell", "email")
    list_filter = ("region",)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ("region", "fname", "tell", "email", "lname")

    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
