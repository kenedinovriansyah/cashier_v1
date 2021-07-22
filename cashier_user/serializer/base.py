
from rest_framework import serializers

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

class Base(BaseUserSerializer):
    class Meta:
        abstract = True