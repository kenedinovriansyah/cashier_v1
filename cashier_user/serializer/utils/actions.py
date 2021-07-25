from database.models.accounts import Address, Phone, Type, choice
from django.contrib.auth.models import User
import os
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.mail import EmailMessage
import dotenv
import uuid

dotenv.load_dotenv()

class UserActions:
    def get_fields(context,fields):
        pass

    def c_u(validated_data,employe):
        if validated_data.get('password') != validated_data.get('password_confirmation'):
            raise serializers.ValidationError({
                'message': _("Password don't match, please check again")
            })
        create = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        create.set_password(validated_data.get('password_confirmation'))
        create.save()
        address = Address(
            public_id=str(uuid.uuid4()),
            country=validated_data.get('country'),
            state=validated_data.get('state'),
            city=validated_data.get('city'),
            address=validated_data.get('address'),
            postal_code=validated_data.get('postal_code'),
            )
        address.save()
        phone = Phone(
            public_id=str(uuid.uuid4()),
            phone_numbers=validated_data.get('phone'),
            phone_fax=validated_data.get('phone_fax')
            )
        phone.save()
        type = Type(
            public_id=str(uuid.uuid4()),
            type=choice.owner,
            )
        type.save()
        create.accounts_set.create(
            avatar=validated_data.get('avatar'),
            gender=validated_data.get('gender'),
            public_id=str(uuid.uuid4()),
            address=address,
            phone=phone,
            type=type
        )
        return create

    def u_u(instance,validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        if instance.username != validated_data.get('username'):
            instance.username = validated_data.get('username')
        accounts = instance.accounts_set.first()
        if accounts:
            accounts.gender = validated_data.get('gender')
            if validated_data.get('avatar'):
                if accounts.avatar:
                    try:
                        splits = str(accounts.avatar).split('/')
                        os.remove('rm media/accounts/%s' % splits[len(splits) - 1])
                    except FileNotFoundError:
                        pass
                accounts.avatar = validated_data.get('avatar')
            # Address
            accounts.address.country = validated_data.get('country')
            accounts.address.state = validated_data.get('state')
            accounts.address.city = validated_data.get('city')
            accounts.address.address = validated_data.get('address')
            accounts.address.postal_code = validated_data.get('postal_code')
            accounts.address.save()
            # Phone
            accounts.phone.phone_numbers = validated_data.get('phone')
            accounts.phone.phone_fax = validated_data.get('phone_fax')
            accounts.phone.save()
            # Type
            accounts.type.type = validated_data.get('type')
            accounts.type.save()
        accounts.save()
        instance.save()
        return instance




    def r_u(validated_data):
        check = User.objects.filter(Q(username=validated_data.get('token'))|Q(email=validated_data.get('token'))).first()
        if not check:
            raise serializers.ValidationError({
                'message': _("Accounts not found")
            })
        mail = EmailMessage("Subject", "Hello Worlds", os.environ.get('username'),[check.email])
        mail.send()
        return mail

    def u_e(instance,validated_data):
        if not instance.check_password(validated_data.get('password')):
            raise serializers.ValidationError({
                'message': _("Password is wrong")
            })
        instance.email = validated_data.get('email')
        instance.save()
        return instance

    def u_p(instance,validated_data):
        if not instance.check_password(validated_data.get('old_password')):
            raise serializers.ValidationError({
                'message': _("Password is wrong")
            })
        if validated_data.get('password') != validated_data.get('password_confirmation'):
            raise serializers.ValidationError({
                'message': _("Password don't match, please check again")
            })
        instance.password = validated_data.get('password')
        instance.set_password(validated_data.get('password_confirmation'))
        instance.save()
        return instance

