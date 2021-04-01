import accounts

from django.conf import settings
from rest_framework import serializers

from core.serializers import (
    ModelSerializer,
)

from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

from . import (
    models,
)


class FileSerializer(ModelSerializer):
    user = accounts.serializers.UsernameSerializer(required=False)

    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'content_type',
            'size',
            'app',
            'key',
            'user',
        ]


class FileUploadSerializer(FileSerializer):
    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'content_type',
            'size',
            'app',
            'key',
            'user',
        ]
        read_only_fields = [
            'content_type',
            'size',
            'user',
        ]
        extra_kwargs = {
            'file': {'required': True},
        }

    def validate(self, attrs):
        if attrs.get('app'):
            if attrs.get('app') not in Const.ATTACHABLE_MODEL_LIST:
                raise serializers.ValidationError(
                    {'app': [Text.INVALID_VALUE]}
                )
        if attrs.get('file').size > settings.UPLOAD_MAX_SIZE:
            raise serializers.ValidationError(
                {'file': [Text.FILE_TOO_LARGE]}
            )

        return attrs

    def create(self, validated_data):
        file = validated_data.get('file')

        instance = self.Meta.model.objects.create(
            user=self.context.get('request').user,
            file=file,
            content_type=file.content_type,
            size=file.size,
            app=validated_data.get('app'),
            key=validated_data.get('key', 0)
        )
        return instance


class FileAttachedSerializer(ModelSerializer):
    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'content_type',
            'size',
        ]
