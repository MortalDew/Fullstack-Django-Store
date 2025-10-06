from django.contrib import admin
from ..models import Product

__all__ = ["ProductAdmin"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock")
    list_filter = ("category",)
    search_fields = ("name", "description")
