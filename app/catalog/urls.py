from django.urls import include, path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path(
        "category/<slug:slug>/",
        ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
