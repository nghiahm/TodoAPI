import pytest
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from users.authentication import ExpiringTokenAuthentication


pytestmark = pytest.mark.django_db


def test_valid_token(user, token):
    """
    Test that a valid token successfully authenticates.
    """
    auth = ExpiringTokenAuthentication()
    user, token = auth.authenticate_credentials(token.key)
    assert user == user
    assert token == token


def test_invalid_token():
    """
    Test that an invalid token raises an exception.
    """
    auth = ExpiringTokenAuthentication()
    with pytest.raises(AuthenticationFailed, match="Invalid token."):
        auth.authenticate_credentials("invalid_token")


def test_inactive_user(user, token):
    """
    Test that an inactive user raises an exception.
    """
    user.is_active = False
    user.save()
    auth = ExpiringTokenAuthentication()
    with pytest.raises(AuthenticationFailed, match="User inactive or deleted."):
        auth.authenticate_credentials(token.key)


def test_expired_token(token):
    """
    Test that an expired token raises an exception.
    """
    token.created = timezone.now() - timezone.timedelta(days=1)
    token.save()
    auth = ExpiringTokenAuthentication()
    with pytest.raises(AuthenticationFailed, match="Token has expired."):
        auth.authenticate_credentials(token.key)
