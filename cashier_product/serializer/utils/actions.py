from rest_framework import serializers
from database.models.category import Category
from database.models.product import Product, TypeProduct, Stock, Currency
import uuid

class ActionsProduct:
    def get_fields(context,fields):
        pass

    def c_p(validated_data):
        pass

    def c_c(validated_data):
        create = Category(
            public_id=str(uuid.uuid4()),
            name=validated_data.get('name'),
            author=validated_data.get('author')
        )
        create.save()
        return create

    def u_p(instance,validated_data):
        pass

    def u_c(instance,validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance

