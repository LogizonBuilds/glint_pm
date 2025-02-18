from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = instance.image.url
        data["image"] = image
        return data


class WhatWeDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "description", "image"]
        read_only_fields = ["created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = instance.image.url
        data["image"] = image
        return data
