import pytest
from rest_framework.authtoken.models import Token
from users.api.views import UserViewSet, ObtainExpiringAuthToken


pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_create_user(self, api_rf):
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

    def test_create_user_missing_field(self, api_rf):
        """
        Test creating a new user with missing fields.
        """
        view = UserViewSet.as_view({"post": "create"})
        data = {"username": "test", "email": "test@example.com"}
        request = api_rf.post("/users/", data)
        response = view(request)
        assert response.status_code == 400

    def test_create_user_existing_username(self, user, api_rf):
        """
        Test creating a new user with an existing username.
        """
        view = UserViewSet.as_view({"post": "create"})
        data = {"username": user.username}
        request = api_rf.post("/users/", data)
        response = view(request)
        assert response.status_code == 400

    def test_get_users(self, user, token, api_rf):
        """
        Test getting a list of users.
        """
        view = UserViewSet.as_view({"get": "list"})
        request = api_rf.get("/users/", HTTP_AUTHORIZATION=f"Token {token.key}")
        response = view(request)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["username"] == user.username

    def test_get_user(self, user, token, api_rf):
        """
        Test getting a user by ID.
        """
        view = UserViewSet.as_view({"get": "retrieve"})
        request = api_rf.get(
            f"/users/{user.id}/", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request, pk=user.id)
        assert response.status_code == 200
        assert response.data["username"] == user.username

    def test_update_user(self, user, token, api_rf):
        """
        Test updating a user by ID.
        """
        view = UserViewSet.as_view({"put": "update"})
        data = {"username": "new_username"}
        request = api_rf.put(
            f"/users/{user.id}/", data, HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request, pk=user.id)
        assert response.status_code == 200
        assert response.data["username"] == "new_username"

    def test_delete_user(self, user, token, api_rf):
        """
        Test deleting a user by ID.
        """
        view = UserViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete(
            f"/users/{user.id}/", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request, pk=user.id)
        assert response.status_code == 204
        assert not Token.objects.filter(user=user).exists()


class TestObtainExpiringAuthToken:
    def test_obtain_auth_token(self, user, token, api_rf):
        """
        Test obtaining an authentication token.
        """
        view = ObtainExpiringAuthToken.as_view()
        data = {"username": user.username, "password": "123"}
        request = api_rf.post("/auth-token/", data)
        response = view(request)
        assert response.status_code == 200
        assert response.data["token"] == token.key

    def test_obtain_auth_token_wrong_password(self, user, api_rf):
        """
        Test obtaining an authentication token with wrong password.
        """
        view = ObtainExpiringAuthToken.as_view()
        data = {"username": user.username, "password": "wrong_password"}
        request = api_rf.post("/auth-token/", data)
        response = view(request)
        assert response.status_code == 400

    def test_obtain_auth_token_user_not_found(self, api_rf):
        """
        Test obtaining an authentication token with user not found.
        """
        view = ObtainExpiringAuthToken.as_view()
        data = {"username": "test", "password": "123"}
        request = api_rf.post("/auth-token/", data)
        response = view(request)
        assert response.status_code == 400
