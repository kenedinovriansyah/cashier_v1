from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from database.models.accounts import choice

class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=225, required=False)
    email = serializers.CharField(max_length=225, required=False)
    first_name = serializers.CharField(max_length=225, required=False)
    last_name = serializers.CharField(max_length=225, required=False)
    old_password = serializers.CharField(max_length=225, required=False)
    password = serializers.CharField(max_length=225, required=False)
    password_confirmation = serializers.CharField(max_length=225, required=False)
    token = serializers.CharField(max_length=225, required=False)

    class Meta:
        abstract = True

class BaseAccountsSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=False)
    gender = serializers.IntegerField(required=False,default=choice.male)

    class Meta:
        abstract = True

class BaseAddressSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=225, required=False)
    state = serializers.CharField(max_length=225, required=False)
    city = serializers.CharField(max_length=225, required=False)
    address = serializers.CharField(max_length=500, required=False)
    postal_code = serializers.CharField(max_length=225, required=False)

    class Meta:
        abstract = True

class BasePhoneSerializer(serializers.Serializer):
    phone_numbers = PhoneNumberField(required=False)
    phone_fax = PhoneNumberField(required=False)

class BaseTypeSerializer(serializers.Serializer):
    type = serializers.IntegerField(default=choice.member, required=False)

    class Meta:
        asbtract = True

class Base(BaseUserSerializer, BasePhoneSerializer, BaseAddressSerializer, BaseTypeSerializer, BaseAccountsSerializer):
    class Meta:
        abstract = True