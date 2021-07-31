from rest_framework import serializers
from database.models.category import Category, SubCategory
from cashier_product.serializer.product import ProductModelSerializer


class SubCategoryModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True, many=True)

    class Meta:
        model = SubCategory
        fields = "__all__"


class CategoryModelSerializer(serializers.ModelSerializer):
    sub = SubCategoryModelSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = "__all__"
