from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from ..models import Category, Product


def product_list(request, slug=None):
    categories = Category.objects.all()
    selected_category = None

    products_qs = Product.objects.select_related("category").all()

    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        products_qs = products_qs.filter(category=selected_category)

    query = request.GET.get("q")
    if query:
        products_qs = products_qs.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(products_qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "page_obj": page_obj,
        "query": query or "",
    }
    return render(request, "catalog/product_list.html", context)


def product_detail(request, pk: int):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})
