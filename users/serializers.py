import re
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from sparky_utils.exceptions import ServiceException

from .models import User


class UserSignupSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, min_length=8)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    whatsapp_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "whatsapp_number",
            "password1",
            "password2",
        )

    def validate_password1(self, password1):
        """Validate user's inputed password on signup

        Args:
            password1 (str): user's password

        Raises:
            serializers.ValidationError: raise password requirements

        Returns:
            str: returns the validated password
        """
        # Regex pattern to match at least one digit, one uppercase letter,
        # one lowercase letter, one special character, and length >= 8
        regex_pattern = (
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(regex_pattern, password1):
            raise serializers.ValidationError(
                "Password must contain at least one digit, "
                "one uppercase letter, one lowercase letter, "
                "one special character, and length >= 8"
            )
        return password1

    def validate(self, data):
        email = data.get("email")
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 != password2:
            raise ServiceException(
                message="The two passwords do not match", status_code=400
            )
        if User.objects.filter(email__iexact=email):
            raise ServiceException(
                message="A client with this email already exists", status_code=409
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        validated_data["password"] = password
        user = User.objects.create(**validated_data)
        return user
