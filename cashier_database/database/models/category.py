from django.db import models
from django.utils import timezone
from .accounts import Accounts
from .product import Product


class SubCategory(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    name = models.CharField(max_length=225, null=False)
    product = models.ManyToManyField(Product, related_name="product_many_to_many")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.update_at = timezone.now()
        super().save(*args, **kwargs)


class Category(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    name = models.CharField(max_length=225, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    sub = models.ManyToManyField(SubCategory, related_name="sub_category_many_to_many")

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
