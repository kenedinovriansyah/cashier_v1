from django.urls import path, include
from rest_framework import routers
from cashier_product.views.product import (
    CategoryModelViewSets,
    CategoryListAPIView,
    ProductModelViewSets,
    UpdateProductAPIView,
    ProductListAPIView,
)

router = routers.DefaultRouter()
router.register("category", CategoryModelViewSets, basename="category")
router.register("product", ProductModelViewSets, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "updated/ext/product/<pk>/",
        UpdateProductAPIView.as_view(),
        name="updated-product",
    ),
    path("category/ext/all/", CategoryListAPIView.as_view(), name="all-category"),
    path("all/", ProductListAPIView.as_view(), name="all-product"),
]
