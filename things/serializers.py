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
            'filename',
            'content_type',
            'size',
            'user',
        ]


class FileUploadSerializer(FileSerializer):
    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'filename',
            'content_type',
            'size',
            'user',
        ]
        read_only_fields = [
            'filename',
            'content_type',
            'size',
            'user',
        ]
        extra_kwargs = {
            'file': {'required': True, 'allow_null': False},
        }

    def validate(self, attrs):
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
            size=file.size
        )
        return instance


class FileIdSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Attachment.objects.all(),
        required=False
    )

    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'filename',
            'content_type',
            'size',
            'created_at',
        ]


class HolidaySerializer(ModelSerializer):
    class Meta:
        model = models.Holiday
        fields = [
            'id',
            'date',
            'name',
        ]
        extra_kwargs = {
            'name': Const.REQUIRED,
        }


class OrderThingSerializer(ModelSerializer):
    class Meta:
        model = models.OrderThing
        fields = (
            'id',
            'order',
            'name',
        )
