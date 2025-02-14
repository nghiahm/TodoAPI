import pytest
from todos.api.views import TodoViewSet
from todos.tests.api.factories import TodoFactory


pytestmark = pytest.mark.django_db


class TestTodoViewSet:
    def test_create_todo(self, token, api_rf):
        """
        Test creating a new todo successfully.
        """
        view = TodoViewSet.as_view({"post": "create"})
        data = {
            "title": "Test Todo",
            "description": "Test Description",
            "completed": False,
        }
        request = api_rf.post("/todos/", data, HTTP_AUTHORIZATION=f"Token {token.key}")
        response = view(request)
        assert response.status_code == 201
        assert response.data["title"] == "Test Todo"
        assert response.data["description"] == "Test Description"

    def test_get_todos(self, user, token, api_rf):
        """
        Test getting a list of todos.
        """
        todos = TodoFactory.create_batch(user=user, size=3)
        view = TodoViewSet.as_view({"get": "list"})
        request = api_rf.get("/todos/", HTTP_AUTHORIZATION=f"Token {token.key}")
        response = view(request)
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]["title"] == todos[0].title

    def test_get_todo(self, todo, token, api_rf):
        """
        Test getting a todo by ID.
        """
        view = TodoViewSet.as_view({"get": "retrieve"})
        request = api_rf.get(
            f"/todos/{todo.id}/", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request, pk=todo.id)
        assert response.status_code == 200
        assert response.data["title"] == todo.title

    def test_update_todo(self, todo, token, api_rf):
        """
        Test updating a todo by ID.
        """
        view = TodoViewSet.as_view({"patch": "partial_update"})
        data = {"title": "Updated Todo"}
        request = api_rf.patch(
            f"/todos/{todo.id}/", data, HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request, pk=todo.id)
        assert response.status_code == 200
        assert response.data["title"] == "Updated Todo"

    def test_delete_todo(self, todo, token, api_rf):
        """
        Test deleting a todo by ID.
        """
        view = TodoViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete(
            f"/todos/{todo.id}/", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request, pk=todo.id)
        assert response.status_code == 204
