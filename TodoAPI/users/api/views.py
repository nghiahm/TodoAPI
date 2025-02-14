import datetime
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, UserCreateSerializer


class UserViewSet(ModelViewSet):
    """
    UserViewSet handles the CRUD operations for User model.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """
        Create a new user and generate an authentication token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {"user": serializer.data, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Create a new token for the user. If the token has expired, delete it and create a new one.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        if not created and token.created < datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(seconds=settings.AUTH_TOKEN_EXPIRATION):
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.now()
            token.save()
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class DeleteAuthTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        """
        Delete the authentication token. This effectively logs the user out.
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
