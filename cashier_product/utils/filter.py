from database.models.category import Category
from django_filters import rest_framework as filters
from database.models.product import Product

class ProductFilterSet(filters.FilterSet):
    name = filters.filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name",]

class CategoryFilterSet(filters.FilterSet):
    name = filters.filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["name",]