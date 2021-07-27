from django.urls import path, include
from rest_framework import routers
from cashier_product.views.product import CategoryModelViewSets

router = routers.DefaultRouter()
router.register('category', CategoryModelViewSets,basename='category')

urlpatterns = [
    path('', include(router.urls))
]