from ..models import Product
from rest_framework.serializers import ModelSerializer
from .categories import CategoryReadSerializer

__all__ = ["ProductReadSerializer"]


class BaseProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "image",
        ]


class ProductReadSerializer(BaseProductSerializer):
    category = CategoryReadSerializer()

    class Meta(BaseProductSerializer.Meta):
        fields = [
            *BaseProductSerializer.Meta.fields,
            "category",
        ]
