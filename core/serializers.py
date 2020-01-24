from rest_framework import serializers


class Serializer(serializers.Serializer):
    pass


class ListSerializer(serializers.ListSerializer):
    pass


class ModelSerializer(serializers.ModelSerializer):
    pass


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    pass
