from rest_framework import serializers
from database.models.category import Category
from database.models.product import Product, TypeProduct, Stock, Currency
import uuid
import os

class ActionsProduct:
    def get_fields(context,fields):
        pass

    def c_p(validated_data):
        stock = Stock(
            public_id=str(uuid.uuid4()),
            stock=validated_data.get('stock'),
            max_stock=validated_data.get('max_stock'),
        )
        stock.save()
        type = TypeProduct(
            public_id=str(uuid.uuid4()),
            type=validated_data.get('type')
        )
        type.save()
        currency = Currency(
            public_id=str(uuid.uuid4()),
            price=validated_data.get('price'),
            sell=validated_data.get('sell')
        )
        currency.save()
        create = Product(
            public_id=str(uuid.uuid4()),
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            icons=validated_data.get('icons'),
            category=validated_data.get('category'),
            stock=stock,
            currency=currency,
            author=validated_data.get('author')
        )
        create.save()
        create.type.add(type)
        validated_data.get('category').product.add(create)
        return create

    def c_c(validated_data):
        create = Category(
            public_id=str(uuid.uuid4()),
            name=validated_data.get('name'),
            author=validated_data.get('author')
        )
        create.save()
        return create

    def u_p(instance,validated_data):
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        if validated_data.get('icons'):
            if instance.icons:
                try:
                    splits = str(instance.icons).split('/')
                    os.remove("rm -rf media/product/%s" % splits[len(splits) - 1])
                except FileNotFoundError:
                    pass
            instance.icons = validated_data.get('icons')
        instance.stock.stock = validated_data.get('stock')
        instance.stock.max_stock = validated_data.get('max_stock')
        instance.stock.save()
        instance.currency.price = validated_data.get('price')
        instance.currency.sell = validated_data.get('sell')
        instance.currency.save()
        type = instance.type.all().filter(public_id=validated_data.get('typeId').public_id).first()
        type.type = validated_data.get('type')
        type.save()
        instance.save()
        return instance


    def u_c(instance,validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance

