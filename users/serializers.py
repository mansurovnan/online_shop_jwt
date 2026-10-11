
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .validators import (
    validate_username,
    validate_email_regex,
    validate_phone_number,
)

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]
        read_only_fields = ["id", "username"]

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        max_length=30,
        validators=[validate_username],
    )

    email = serializers.CharField(
        validators=[validate_email_regex],
    )

    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[validate_phone_number],
    )

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "password2",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password2": "Parollar bir xil emas."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.RegexField(
        regex=r"^[A-Za-z0-9_]{3,30}$",
        error_messages={
            "invalid": "Username formati noto'g'ri."
        },
    )

