from .views import CART_SESSION_KEY


def cart_item_count(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    try:
        count = sum(int(item.get("quantity", 0)) for item in cart.values())
    except Exception:
        count = 0
    return {"cart_item_count": count}
