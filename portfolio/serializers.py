from rest_framework import serializers
from .models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = instance.image.url
        data["image"] = image
        return data
