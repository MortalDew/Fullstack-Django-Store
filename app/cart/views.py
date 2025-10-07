from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from app.catalog.models import Product

CART_SESSION_KEY = "cart"


def _get_cart(session) -> dict:
    cart = session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


@login_required
@require_POST
def cart_add(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))

    # Disallow adding if nothing in stock
    if product.stock <= 0:
        return redirect("cart_detail")

    cart = _get_cart(request.session)
    key = str(product.pk)
    existing_qty = int(cart.get(key, {}).get("quantity", 0))

    # Cap by available stock
    new_qty = existing_qty + max(quantity, 1)
    if new_qty > product.stock:
        new_qty = product.stock

    cart[key] = {"quantity": new_qty, "price": str(product.price)}
    request.session.modified = True
    return redirect("cart_detail")


@login_required
@require_POST
def cart_update(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = _get_cart(request.session)
    key = str(product.pk)

    # Normalize to [0, stock]
    if quantity <= 0:
        cart.pop(key, None)
    else:
        capped = min(quantity, max(product.stock, 0))
        if capped <= 0:
            cart.pop(key, None)
        else:
            cart[key] = {"quantity": capped, "price": str(product.price)}
    request.session.modified = True
    return redirect("cart_detail")


@login_required
@require_POST
def cart_remove(request, product_id: int):
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    cart = _get_cart(request.session)
    product_ids = [int(pid) for pid in cart.keys()]
    products = {p.pk: p for p in Product.objects.filter(pk__in=product_ids)}

    items = []
    total = Decimal("0.00")
    for pid, data in cart.items():
        product = products.get(int(pid))
        if not product:
            continue
        quantity = int(data.get("quantity", 0))
        # Cap displayed quantity as well, in case stock changed
        if quantity > product.stock:
            quantity = product.stock
            cart[str(product.pk)] = {"quantity": quantity, "price": str(product.price)}
            request.session.modified = True
        price = Decimal(str(data.get("price", product.price)))
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
