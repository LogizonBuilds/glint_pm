from rest_framework import serializers
from .models import Portfolio, AboutUs


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = instance.image.url
        data["image"] = image
        return data


class AboutUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = instance.image.url
        data["image"] = image
        return data
