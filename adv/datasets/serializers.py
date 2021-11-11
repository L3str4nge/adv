from rest_framework import serializers
from .models import Dataset


class DatasetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "created"]


class DatasetSerializer(serializers.ModelSerializer):
    content = serializers.ReadOnlyField()

    class Meta:
        model = Dataset
        fields = ["id", "created", "content"]


class DatasetHeaderSerializer(serializers.ModelSerializer):
    headers = serializers.ReadOnlyField()

    class Meta:
        model = Dataset
        fields = ["id", "created", "headers"]
