import ast
from database.models.category import Category
from database.models.product import Product, TypeProduct, Stock, Currency, ProductImage
import uuid
import os


class ActionsProduct:
    def get_fields(context, fields):
        pass

    def c_p(validated_data):
        stock = Stock(
            public_id=str(uuid.uuid4()),
            stock=validated_data.get("stock"),
            max_stock=validated_data.get("max_stock"),
        )
        stock.save()
        type = TypeProduct(public_id=str(uuid.uuid4()), type=validated_data.get("type"))
        type.save()
        currency = Currency(
            public_id=str(uuid.uuid4()),
            price=validated_data.get("price"),
            sales_price=validated_data.get("sell"),
        )
        currency.save()
        create = Product(
            public_id=str(uuid.uuid4()),
            name=validated_data.get("name"),
            desc=validated_data.get("description"),
            category=validated_data.get("category"),
            stock=stock,
            currency=currency,
            author=validated_data.get("author"),
        )
        create.save()
        create.type.add(type)
        validated_data.get("category").product.add(create)
        return create

    def p_a_image(instance, validated_data):
        image = ProductImage(
            public_id=str(uuid.uuid4()),
            picture=validated_data.get("image"),
            hex=validated_data.get("hex"),
        )
        image.save()
        instance.galery.add(image)
        return instance

    def u_a_image(instance, validated_data):
        if instance.picture:
            os.system('rm media/%s' % instance.picture)
        instance.picture = validated_data.get("image")
        instance.hex = validated_data.get("hex")
        instance.save()
        return instance

    def c_c(validated_data):
        create = Category(
            public_id=str(uuid.uuid4()),
            name=validated_data.get("name"),
            author=validated_data.get("author"),
        )
        create.save()
        return create

    def u_p(instance, validated_data):
        instance.name = validated_data.get("name")
        instance.description = validated_data.get("description")
        instance.stock.stock = validated_data.get("stock")
        instance.stock.max_stock = validated_data.get("max_stock")
        instance.stock.save()
        instance.currency.price = validated_data.get("price")
        instance.currency.sell = validated_data.get("sell")
        instance.currency.save()
        type = (
            instance.type.all()
            .filter(public_id=validated_data.get("typeId").public_id)
            .first()
        )
        type.type = validated_data.get("type")
        type.save()
        instance.save()
        return instance

    def u_c(instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()
        return instance
