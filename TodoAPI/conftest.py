import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from users.tests.api.factories import UserFactory


@pytest.fixture
def api_rf() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def user(db) -> User:
    return UserFactory(password="123")


@pytest.fixture
def token(user) -> Token:
    return Token.objects.create(user=user)
