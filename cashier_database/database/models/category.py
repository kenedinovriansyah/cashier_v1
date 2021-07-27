from django.db import models
from django.utils import timezone
from .accounts import Accounts
from .product import Product


class Category(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    name = models.CharField(max_length=225, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    product = models.ManyToManyField(Product, related_name="product_many_to_many")
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
