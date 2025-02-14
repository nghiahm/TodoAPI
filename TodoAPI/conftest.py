import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from users.tests.api.factories import UserFactory
from todos.models import Todo
from todos.tests.api.factories import TodoFactory


@pytest.fixture
def api_rf() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def user(db) -> User:
    return UserFactory(password="123")


@pytest.fixture
def token(user) -> Token:
    return Token.objects.create(user=user)


@pytest.fixture
def todo(user) -> Todo:
    return TodoFactory(user=user)
