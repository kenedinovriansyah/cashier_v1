from database.models.accounts import Accounts
from database.models.category import Category
from database.models.product import TypeProduct
from rest_framework import serializers


class BaseCategory(serializers.Serializer):
    name = serializers.CharField(max_length=225, required=False)

    class Meta:
        abstract = True


class BaseStock(serializers.Serializer):
    stock = serializers.IntegerField(default=0)
    max_stock = serializers.IntegerField(default=0)
    sold = serializers.BooleanField(default=False)

    class Meta:
        abstract = True


class BaseTypeProduct(serializers.Serializer):
    type = serializers.CharField(max_length=225, required=False)
    typeId = serializers.PrimaryKeyRelatedField(
        queryset=TypeProduct.objects.all(), required=False
    )

    class Meta:
        abstract = True


class BaseCurrency(serializers.Serializer):
    price = serializers.DecimalField(required=False, decimal_places=2, max_digits=8)
    sell = serializers.DecimalField(required=False, decimal_places=2, max_digits=8)

    class Meta:
        abstract = True


class BaseProduct(serializers.Serializer):
    icons = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=Accounts.objects.all(), required=False
    )

    class Meta:
        abstract = True


class Base(BaseCategory, BaseStock, BaseTypeProduct, BaseCurrency, BaseProduct):
    class Meta:
        abstract = True
