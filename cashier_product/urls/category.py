from django.urls import path, include
from cashier_product.views.product import (
    SubCategoryGenericUpdateorDestroy,
    CategoryListAPIView,
    CategoryModelViewSets,
)
from rest_framework import routers

router = routers.DefaultRouter()

router.register("", CategoryModelViewSets, basename="category")

urlpatterns = [
    path(
        "sub/<pk>/",
        SubCategoryGenericUpdateorDestroy.as_view(),
        name="sub-category-detail",
    ),
    path("ext/all/", CategoryListAPIView.as_view(), name="all-category"),
    path("", include(router.urls)),
]
