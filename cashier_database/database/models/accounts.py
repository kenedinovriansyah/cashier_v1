from django.db import models
from .base import Base
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class choice:
    male = 0
    female = 1
    member = 0
    staff = 1
    owner = 2
    gender = ((male,_("Male")),(female,_("Female")))
    type_accounts = ((member,_("Member")),(staff,_("Staff")),(owner,_("Owner")))

class Type(models.Model):
    public_id = models.CharField(max_length=225, null=False ,unique=True)
    type = models.IntegerField(choices=choice.type_accounts, default=choice.member)

class Phone(models.Model):
    public_id = models.CharField(max_length=225, null=False ,unique=True)
    phone_numbers = PhoneNumberField(blank=True, null=True, unique=False)
    phone_fax = PhoneNumberField(blank=True, null=True)

class Address(models.Model):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    country = models.CharField(max_length=225, null=True)
    state = models.CharField(max_length=225, null=True)
    city = models.CharField(max_length=225, null=True)
    address = models.CharField(max_length=225, null=True)
    postal_code = models.CharField(max_length=225, null=True)

class Accounts(Base):
    public_id = models.CharField(max_length=225, null=False, unique=True)
    avatar = models.ImageField(upload_to="accounts/", null=True)
    gender = models.IntegerField(choices=choice.gender, default=choice.male)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    employe = models.ManyToManyField(User, related_name='employe_or_member_many_to_many')

    def save(self, *args, **kwargs):
        self.update_at = timezone.now()
        super().save(*args,**kwargs)