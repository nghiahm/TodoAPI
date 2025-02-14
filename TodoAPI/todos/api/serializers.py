from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from todos.models import Todo


class TodoSerializer(ModelSerializer):
    """
    Serializer for the Todo model.
    """

    class Meta:
        model = Todo
        fields = "__all__"


class TodoCreateSerializer(ModelSerializer):
    """
    Serializer for creating a new Todo.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Todo
        fields = "__all__"
