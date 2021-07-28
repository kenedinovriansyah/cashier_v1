from cashier_product.serializer.product import (
    CategoryModelSerializer,
    ProductModelSerializer,
    ProductSerializer,
)
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from database.models.category import Category
from database.models.product import Product
from django.utils.translation import gettext as _
from django.conf import settings
from core.utils.pagination import StandardResultsSetPagination


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny,]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny,]


class CategoryModelViewSets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    fields_serializer = ProductSerializer

    def list(self, request, *args, **kwargs):
        pass

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [
                permissions.AllowAny,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.fields_serializer(data=request.data)
        serializer.context["types"] = "create-category"
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": _("Category has been created"),
                    "data": self.serializer_class(
                        Category.objects.filter(
                            author__id=request.data.get("author")
                        ).first()
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = self.get_queryset().filter(public_id=pk).first()
        if not queryset:
            return Response(
                {"message": _("Category not found")}, status=status.HTTP_404_NOT_FOUND
            )
        if not settings.TEST:
            queryset.delete()
        return Response(
            {"message": _("Category has been deleted")}, status=status.HTTP_200_OK
        )

    def update(self, request, pk):
        queryset = self.get_queryset().filter(public_id=pk).first()
        if not queryset:
            return Response(
                {"message": _("Category not found")}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.fields_serializer(queryset, data=request.data)
        serializer.context["types"] = "updated-category"
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": _("Category has been updated"),
                    "data": self.serializer_class(
                        Category.objects.filter(public_id=pk).first()
                    ).data,
                },
                status=status.HTTP_200_OK,
            )


class ProductModelViewSets(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    fields_serializer = ProductSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [
                permissions.AllowAny,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request):
        serializer = self.fields_serializer(data=request.data)
        serializer.context["types"] = "create-product"
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": _("Product has been created"),
                    "data": self.serializer_class(
                        Product.objects.filter(
                            author__id=request.data.get("author")
                        ).first()
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = self.get_queryset().filter(public_id=pk).first()
        if not queryset:
            return Response(
                {"message": _("Product not found")}, status=status.HTTP_404_NOT_FOUND
            )
        if not settings.TEST:
            queryset.delete()
        return Response(
            {"message": _("Product has been deleted")}, status=status.HTTP_200_OK
        )


class UpdateProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    fields_serializer = ProductSerializer

    def post(self, request, pk):
        queryset = self.queryset.filter(public_id=pk).first()
        serializer = self.fields_serializer(queryset, data=request.data)
        serializer.context["types"] = "updated-product"
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": _("Product has been updated"),
                    "data": self.serializer_class(
                        Product.objects.filter(public_id=pk).first()
                    ).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
