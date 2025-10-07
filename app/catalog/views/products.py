from typing import Any
from django.db.models import QuerySet, Q
from app.base.cache import BaseDispatchCache
from django.views.generic import ListView, DetailView
from ..models import Product, Category

__all__ = ["ProductListView", "ProductDetailView"]


class ProductListView(BaseDispatchCache, ListView):
    template_name = "catalog/product_list.html"
    model = Product
    context_object_name = "products"
    paginate_by = 8
    cache_timeout = 120

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = Product.objects.select_related("category").all()
        slug: str | None = self.kwargs.get("slug")
        if slug:
            queryset = queryset.filter(category__slug=slug)
        query: str | None = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        slug: str | None = self.kwargs.get("slug")
        context["selected_category"] = (
            Category.objects.filter(slug=slug).first() if slug else None
        )
        context["query"] = self.request.GET.get("q", "")
        return context


class ProductDetailView(DetailView):
    template_name = "catalog/product_detail.html"
    model = Product
    context_object_name = "product"
