from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from requestor.models import Requestor
from .models import *


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )

        role, _ = Role.objects.get_or_create(name="REQUESTOR")
        user.role = role
        user.save()

        requestor = Requestor.objects.create(user=user)

        return requestor


class MyCustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role.name

        return token


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
