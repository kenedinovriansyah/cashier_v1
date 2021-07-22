from database.models.accounts import Address, Type, Phone, Accounts
from rest_framework import serializers
from django.contrib.auth.models import User
from .base import Base
from .utils.actions import UserActions

class UserSerializers(Base):
    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.actions = UserActions

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        self.actions.get_fields(self.context,fields)
        return fields

    def create(self, validated_data):
        if self.context['types'] == 'create':
            return self.actions.c_u(validated_data)
        elif self.context['types'] == 'reset':
            return self.actions.r_u(validated_data)
        pass

    def update(self, instance, validated_data):
        if self.context['types'] == 'updated':
            return self.actions.u_u(instance,validated_data)
        elif self.context['types'] == 'password':
            return self.actions.u_p(instance,validated_data)
        elif self.context['types'] == 'email':
            return self.actions.u_e(instance,validated_data)
        elif self.context['types'] == 'employe':
            # Create Employe
            accounts = self.actions.c_u(validated_data)
            instance.accounts_set.first().employe.add(accounts)
            return instance

class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
    

class PhoneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

class TypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

    name = serializers.SerializerMethodField('get_name_display')

    def get_name_display(self, context):
        return context.get_type_display()


class AccountsEmployeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"

class UserEmployeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    accounts = serializers.SerializerMethodField('get_accounts_display')

    def get_accounts_display(self, context):
        return AccountsModelSerializer(context.accounts_set.first()).data

class AccountsModelSerializer(serializers.ModelSerializer):
    phone = PhoneModelSerializer(read_only=True)
    address = AddressModelSerializer(read_only=True)
    type = TypeModelSerializer(read_only=True)
    employe = UserEmployeModelSerializer(read_only=True, many=True)

    class Meta:
        model = Accounts
        fields = "__all__"

    name_gender = serializers.SerializerMethodField("get_gender_display")

    def get_gender_display(self,context):
        return context.get_gender_display()
    


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    
    accounts = serializers.SerializerMethodField('get_accounts_display')

    def get_accounts_display(self, context):
        return AccountsModelSerializer(context.accounts_set.first()).data