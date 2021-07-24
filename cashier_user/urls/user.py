from cashier_user.views.user import UserModelViewSets, UpdateUserAPIView,AccountsMeAPIView, UpdateEmployeAPIView
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', UserModelViewSets, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('updated/accounts/', UpdateUserAPIView.as_view(), name='updated-accounts'),
    path('updated/accounts/employe/<pk>/', UpdateEmployeAPIView.as_view(),name="updated-employe"),
    path('accounts/me/', AccountsMeAPIView.as_view(), name='me')
]