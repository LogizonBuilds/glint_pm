from rest_framework import serializers
from .models import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image_url = instance.image.url
        data["image"] = image_url
        return data
