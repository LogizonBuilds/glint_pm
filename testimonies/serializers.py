from rest_framework import serializers
from .models import Testimony


class TestimonySerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    testimony = serializers.CharField(required=True)

    class Meta:
        model = Testimony
        fields = ("full_name", "role", "testimony")
