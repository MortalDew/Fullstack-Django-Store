from django.conf import settings
from django.db import models

__all__ = ["CartItem"]


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="in_carts",
    )
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self) -> str:
        return f"{self.user} → {self.product} x {self.quantity}"
