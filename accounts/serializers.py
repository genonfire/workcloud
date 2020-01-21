from django.contrib.auth import (
    authenticate,
    password_validation
)

from rest_framework import serializers

from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

from . import models, tools


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'call_name'
        ]
        read_only_fields = ['call_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')

        call_name = tools.get_call_name(
            validated_data.get('first_name'),
            validated_data.get('last_name'),
            request.LANGUAGE_CODE
        )

        user = self.Meta.model.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('username'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            call_name=call_name,
            is_approved=True
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=Const.EMAIL_MAX_LENGTH)
    password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)

    def authenticate(self, **kwargs):
        return authenticate(self.context.get('request'), **kwargs)

    def validate(self, data):
        user = self.authenticate(
            username=data.get('username'),
            password=data.get('password')
        )

        if not user:
            raise serializers.ValidationError(Text.UNABLE_TO_LOGIN)
        else:
            if not user.is_active:
                raise serializers.ValidationError(Text.USER_IS_DEACTIVATED)

        data['user'] = user
        return data


class LoginDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LoginDevice
        fields = [
            'id',
            'user',
            'device',
            'os',
            'browser',
            'ip_address',
            'last_login',
            'is_registered'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)
    new_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def validate(self, data):
        if not self.user.check_password(data.get('old_password')):
            raise serializers.ValidationError(Text.INVALID_PASSWORD)
        if data.get('old_password') == data.get('new_password'):
            raise serializers.ValidationError(Text.SAME_AS_OLD_PASSWORD)

        password_validation.validate_password(
            data.get('new_password'), self.user)

        return data

    def save(self):
        self.user.set_password(self.validated_data.get('new_password'))
        self.user.save(update_fields=['password'])
        self.user.token().delete()
        devices = models.LoginDevice.objects.filter(user=self.user)
        devices.delete()
