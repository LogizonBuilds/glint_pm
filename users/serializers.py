import re
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from sparky_utils.exceptions import ServiceException

from .models import User, Setting, Transaction


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
        print("Password Register: ", password)
        validated_data.pop("password2")
        validated_data["password"] = password
        user = User.objects.create_user(**validated_data)
        return user


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class UserDetailsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "last_name",
            "whatsapp_number",
            "date_joined",
            "is_active",
            "residential_address",
            "profile_pic",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        full_name = instance.full_name
        data["full_name"] = full_name
        return data


class ChangePasswordUnAuthenticatedSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

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
        password1 = data.get("password1")
        email = data.get("email")
        password2 = data.get("password2")

        if str(password1) != str(password2):
            raise ServiceException(message="Password Do not match", status_code=400)
        # check id user exist
        if not User.objects.filter(email__iexact=email).exists():
            raise ServiceException(message="User does not exist", status_code=404)
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # get user
        user = User.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            data["user"] = user
            return data
        else:
            raise ServiceException(message="Invalid credentials", status_code=401)


class UpdateUserSerializer(serializers.Serializer):
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    whatsapp_number = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    residential_address = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class ChangePasswordAuthenticatedSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_new_password(self, new_password):
        """Validate user's inputed password on change password"""
        # Regex pattern to match at least one digit, one uppercase letter,
        # one lowercase letter, one special character, and length >= 8
        regex_pattern = (
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(regex_pattern, new_password):
            raise serializers.ValidationError(
                "Password must contain at least one digit, "
                "one uppercase letter, one lowercase letter, "
                "one special character, and length >= 8"
            )
        return new_password

    def validate(self, data):
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if new_password != confirm_password:
            raise ServiceException(
                message="The two passwords do not match", status_code=400
            )

        return data


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "amount",
            "service_name",
            "transaction_date",
            "transaction_status",
            "transaction_description",
            "transaction_reference",
            "transaction_currency",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        username = instance.user.full_name
        data["username"] = username
        return data
