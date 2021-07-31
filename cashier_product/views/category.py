import os
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cashier_product.utils.filter import CategoryFilterSet
from cashier_product.serializer.category import (
    CategoryModelSerializer,
    SubCategoryModelSerializer,
)
from cashier_product.serializer.product import ProductSerializer
from database.models.category import Category, SubCategory
from django.conf import settings
from core.utils.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, generics


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [
        permissions.AllowAny,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = CategoryFilterSet


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
        if request.data.get("types") == "sub-category":
            serializer.context["types"] = "sub-category"
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
            for i in queryset.galery.all():
                os.system("rm media/%s" % i.image)
                i.delete()
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


class SubCategoryGenericUpdateorDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryModelSerializer
    fields_serializer = ProductSerializer

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
        serializer.context["types"] = "sub-category-update"
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": _("Category has been updated"),
                    "data": self.serializer_class(
                        SubCategory.objects.filter(public_id=pk).first()
                    ).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
