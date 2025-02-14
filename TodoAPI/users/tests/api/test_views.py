import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from users.api.views import UserViewSet


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    @pytest.mark.django_db
    def test_create_user(self, api_rf: APIRequestFactory):
        """
        Test creating a new user.
        """
        view = UserViewSet.as_view({"post": "create"})
        data = {"username": "test", "email": "test@example.com", "password": "123"}
        request = api_rf.post("/users/", data)
        response = view(request)
        assert response.status_code == 201
        assert response.data["user"]["username"] == "test"
        assert response.data["token"] == Token.objects.get(user__username="test").key

    @pytest.mark.django_db
    def test_create_user_missing_field(self, api_rf: APIRequestFactory):
        """
        Test creating a new user with missing fields.
        """
        view = UserViewSet.as_view({"post": "create"})
        data = {"username": "test", "email": "test@example.com"}
        request = api_rf.post("/users/", data)
        response = view(request)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_user_existing_username(self, user, api_rf: APIRequestFactory):
        """
        Test creating a new user with an existing username.
        """
        view = UserViewSet.as_view({"post": "create"})
        data = {"username": user.username}
        request = api_rf.post("/users/", data)
        response = view(request)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_users(self, user, api_rf: APIRequestFactory):
        """
        Test getting a list of users.
        """
        view = UserViewSet.as_view({"get": "list"})
        request = api_rf.get("/users/")
        response = view(request)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["username"] == user.username

    @pytest.mark.django_db
    def test_get_user(self, user, api_rf: APIRequestFactory):
        """
        Test getting a user by ID.
        """
        view = UserViewSet.as_view({"get": "retrieve"})
        request = api_rf.get(f"/users/{user.id}/")
        response = view(request, pk=user.id)
        assert response.status_code == 200
        assert response.data["username"] == user.username

    @pytest.mark.django_db
    def test_update_user(self, user, api_rf: APIRequestFactory):
        """
        Test updating a user by ID.
        """
        view = UserViewSet.as_view({"put": "update"})
        data = {"username": "new_username"}
        request = api_rf.put(f"/users/{user.id}/", data)
        response = view(request, pk=user.id)
        assert response.status_code == 200
        assert response.data["username"] == "new_username"

    @pytest.mark.django_db
    def test_delete_user(self, user, api_rf: APIRequestFactory):
        """
        Test deleting a user by ID.
        """
        view = UserViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete(f"/users/{user.id}/")
        response = view(request, pk=user.id)
        assert response.status_code == 204
        assert not Token.objects.filter(user=user).exists()
