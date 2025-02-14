from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from todos.api.serializers import TodoSerializer, TodoCreateSerializer
from todos.models import Todo


class TodoViewSet(ModelViewSet):
    """
    TodoViewSet handles the CRUD operations for Todo model.
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return TodoCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
