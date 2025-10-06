from django.urls import include, path
from .views import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("category/<slug:slug>/", views.product_list, name="product_list_by_category"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
]
