from django.db.models import QuerySet
from rest_framework.views import Response
from ..models import Category
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.views.generic import TemplateView
from ..serializers.categories import CategoryReadSerializer

__all__ = ["CategoryListView"]


class CategoryListView(ListModelMixin, TemplateView):
    template_name = "catalog/category_list.html"
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
