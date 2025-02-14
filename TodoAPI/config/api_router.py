from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from users.api.views import UserViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
urlpatterns = router.urls

urlpatterns += [
    path("auth-token/", obtain_auth_token),
]
