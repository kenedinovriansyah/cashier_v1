from django.urls import path, include
from rest_framework import routers
from cashier_product.views.product import CategoryModelViewSets, ProductModelViewSets,UpdateProductAPIView

router = routers.DefaultRouter()
router.register('category', CategoryModelViewSets,basename='category')
router.register('product', ProductModelViewSets,basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('updated/ext/product/<pk>/', UpdateProductAPIView.as_view(), name='updated-product')
]