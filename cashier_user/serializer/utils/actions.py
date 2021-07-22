from django.contrib.auth.models import User
import os
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.mail import EmailMessage
import dotenv

dotenv.load_dotenv()

class UserActions:
    def get_fields(context,fields):
        pass

    def c_u(validated_data):
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
        return create

    def u_u(instance,validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        accounts = instance.accounts_set.first()
        if accounts:
            pass
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
