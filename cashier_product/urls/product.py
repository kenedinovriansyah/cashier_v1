from os import name
from django.urls import path, include
from rest_framework import routers
from cashier_product.views.product import (
    ProductModelViewSets,
    UpdateProductAPIView,
    ProductListAPIView,
    ProductGenericCreateAPIView,
    UpdateProductImageCreateAPIView,
    CodeProductCreateAPIView,
)

router = routers.DefaultRouter()
router.register("product", ProductModelViewSets, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "updated/ext/product/<pk>/",
        UpdateProductAPIView.as_view(),
        name="updated-product",
    ),
    path("all/", ProductListAPIView.as_view(), name="all-product"),
    path(
        "add/image/to/product/<pk>/",
        ProductGenericCreateAPIView.as_view(),
        name="add-image-to-product",
    ),
    path(
        "updated/image/to/product/<pk>/",
        UpdateProductImageCreateAPIView.as_view(),
        name="updated-image-to-product",
    ),
    path("code/", CodeProductCreateAPIView.as_view(), name="create-product-code"),
]
