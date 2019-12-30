from rest_framework import serializers

from utils.debug import Debug  # noqa

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
