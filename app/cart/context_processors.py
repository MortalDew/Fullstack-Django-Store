from django.core.cache import cache
from .models import CartItem


def cart_item_count(request):
    if not request.user.is_authenticated:
        return {"cart_item_count": 0}
    cache_key = f"cart:count:user:{request.user.pk}"
    count = cache.get(cache_key)
    if count is None:
        try:
            count = sum(
                item.quantity for item in CartItem.objects.filter(user=request.user)
            )
        except Exception:
            count = 0
        cache.set(cache_key, int(count), timeout=120)
    return {"cart_item_count": int(count)}
