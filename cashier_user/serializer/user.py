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
        return super().update(instance, validated_data)

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        models = User.objects.all()
        fields = "__all__"

