from django.contrib import admin
from ..models import CartItem

__all__ = ["CartItemAdmin"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "price")
    list_filter = ("product", "user")
