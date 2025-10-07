from decimal import Decimal
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from app.catalog.models import Product
from .models import CartItem

__all__ = ["cart_add", "cart_update", "cart_remove", "cart_detail"]


@login_required
@require_POST
def cart_add(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))

    # Disallow adding if nothing in stock
    if product.stock <= 0:
        return redirect("cart_detail")

    # Determine new quantity based on existing DB item
    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={
            "quantity": max(1, min(quantity, product.stock)),
            "price": product.price,
        },
    )
    if not created:
        new_qty = min(product.stock, item.quantity + max(1, quantity))
        if new_qty != item.quantity or item.price != product.price:
            item.quantity = new_qty
            item.price = product.price
            item.save(update_fields=["quantity", "price"])
    # Invalidate cart caches for this user
    cache.delete(f"cart:count:user:{request.user.pk}")
    cache.delete(f"cart:items:user:{request.user.pk}")
    return redirect("cart_detail")


@login_required
@require_POST
def cart_update(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    # Normalize to [0, stock]
    if quantity <= 0:
        CartItem.objects.filter(user=request.user, product=product).delete()
    else:
        capped = min(quantity, max(product.stock, 0))
        if capped <= 0:
            CartItem.objects.filter(user=request.user, product=product).delete()
        else:
            item, _ = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={"quantity": capped, "price": product.price},
            )
            if item.quantity != capped or item.price != product.price:
                item.quantity = capped
                item.price = product.price
                item.save(update_fields=["quantity", "price"])
    cache.delete(f"cart:count:user:{request.user.pk}")
    cache.delete(f"cart:items:user:{request.user.pk}")
    return redirect("cart_detail")


@login_required
@require_POST
def cart_remove(request, product_id: int):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    cache.delete(f"cart:count:user:{request.user.pk}")
    cache.delete(f"cart:items:user:{request.user.pk}")
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    cache_key = f"cart:items:user:{request.user.pk}"
    db_items = cache.get(cache_key)
    if db_items is None:
        db_items = list(
            CartItem.objects.filter(user=request.user).select_related("product")
        )
        cache.set(cache_key, db_items, timeout=120)

    items = []
    total = Decimal("0.00")
    for item in db_items:
        product = item.product
        quantity = min(item.quantity, max(product.stock, 0))
        price = Decimal(str(item.price))
        line_total = price * quantity
        total += line_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "price": price,
                "line_total": line_total,
                "stock": product.stock,
            }
        )

    note = request.POST.get("note") if request.method == "POST" else ""

    return render(
        request,
        "cart/cart_detail.html",
        {
            "items": items,
            "total": total,
            "note": note,
        },
    )
