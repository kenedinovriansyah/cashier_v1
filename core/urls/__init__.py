from django.urls import path, include

urlpatterns = [
    path("user/", include("cashier_user.urls.user")),
    path("product/", include("cashier_product.urls.product")),
    path("category/", include("cashier_product.urls.category")),
    path("default/", include("cashier_default.urls.default")),
]
