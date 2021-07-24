from django.urls import path, include
from cashier_default.views.default import DefaultAPIView

urlpatterns = [
    path('', DefaultAPIView.as_view(), name='employe')
]