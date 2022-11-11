from server.exceptions import UniqueException
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=14)
    password = serializers.CharField(max_length=100, write_only=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_cpf(self, cpf: str):
        cpf_exists = User.objects.filter(cpf=cpf).exists()

        if cpf_exists:
            raise UniqueException({"detail": ["CPF already exists."]})

        return cpf

    def validate_email(self, email: str):
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise UniqueException({"detail": ["Email already exists."]})

        return email

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()
