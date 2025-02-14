from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication that checks if the token has expired.
    """

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related("user").get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        if settings.AUTH_TOKEN_EXPIRATION:
            expiration_time = token.created + timedelta(
                seconds=settings.AUTH_TOKEN_EXPIRATION
            )
            if expiration_time < timezone.now():
                raise AuthenticationFailed("Token has expired.")

        return token.user, token
