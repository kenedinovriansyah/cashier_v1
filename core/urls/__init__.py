from django.urls import path, include

urlpatterns = [
    path('user/', include('cashier_user.urls.user'))
]