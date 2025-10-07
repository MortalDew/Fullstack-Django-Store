from ..models import Category
from rest_framework.serializers import ModelSerializer

__all__ = ["CategoryReadSerializer"]


class BaseCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class CategoryReadSerializer(BaseCategorySerializer):
    pass
