from database.models.category import Category
from database.models.product import Product, Stock, TypeProduct, Currency, ProductImage
from rest_framework import serializers
from .base import Base
from .utils.actions import ActionsProduct
from babel.numbers import format_currency
from cashier_user.serializer.user import ChildAccountsModelSerializer


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
        elif self.context['types'] == 'add-image-at-product':
            return self.actions.p_a_image(instance,validated_data)
        elif self.context['types'] == 'updated-image-at-product':
            return self.actions.u_a_image(instance,validated_data)
        pass


class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ["id"]


class TypeProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduct
        exclude = ["id"]


class CurrencyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ["id"]

    price_currency = serializers.SerializerMethodField("get_price_currency_display")
    sell_currency = serializers.SerializerMethodField("get_sell_currency_display")

    def get_price_currency_display(self, context):
        return format_currency(context.price, "IDR", locale="id_ID")

    def get_sell_currency_display(self, context):
        return format_currency(context.sell, "IDR", locale="id_ID")

class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id"]

class ProductModelSerializer(serializers.ModelSerializer):
    stock = StockModelSerializer(read_only=True)
    currency = CurrencyModelSerializer(read_only=True)
    type = TypeProductModelSerializer(read_only=True, many=True)
    author = ChildAccountsModelSerializer(read_only=True)
    galery = ProductImageModelSerializer(read_only=True,many=True)

    class Meta:
        model = Product
        exclude = ["id", "category"]


class CategoryModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = "__all__"
