from django.db import models
from .accounts import Accounts
from django.utils import timezone

class Stock(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    stock = models.IntegerField(default=0)
    max_stock = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)

class TypeProduct(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    type = models.CharField(max_length=225, null=False)

class Currency(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    price = models.DecimalField(decimal_places=2,max_digits=12)
    sell = models.DecimalField(decimal_places=2,max_digits=12)

class Product(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    name = models.CharField(max_length=225, null=False)
    description = models.TextField(null=False)
    type = models.ManyToManyField(TypeProduct, related_name='type_many_to_many')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='+')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
