from database.models.category import Category
from database.models.product import Product, Stock, TypeProduct, Currency
from rest_framework import serializers
from .base import Base
from .utils.actions import ActionsProduct


class ProductSerializer(Base):
    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.actions = ActionsProduct

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        return fields

    def create(self, validated_data):
        if self.context["types"] == "create-category":
            return self.actions.c_c(validated_data)
        elif self.context["types"] == "create-product":
            return self.actions.c_p(validated_data)
        pass

    def update(self, instance, validated_data):
        if self.context["types"] == "updated-category":
            return self.actions.u_c(instance, validated_data)
        elif self.context["types"] == "updated-product":
            return self.actions.u_p(instance, validated_data)
        pass


class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class TypeProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduct
        fields = "__all__"


class CurrencyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class ProductModelSerializer(serializers.ModelSerializer):
    stock = StockModelSerializer(read_only=True)
    currency = CurrencyModelSerializer(read_only=True)
    type = TypeProductModelSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = "__all__"


class CategoryModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = "__all__"
