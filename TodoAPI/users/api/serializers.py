from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    Serializer for User model.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class UserCreateSerializer(ModelSerializer):
    """
    Serializer for creating a new user.
    """

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
