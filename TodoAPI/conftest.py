import pytest
from django.contrib.auth.models import User
from users.tests.api.factories import UserFactory


@pytest.fixture
def user(db) -> User:
    return UserFactory()
