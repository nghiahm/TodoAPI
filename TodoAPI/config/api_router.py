from django.urls import path
from rest_framework.routers import DefaultRouter
from users.api.views import UserViewSet, ObtainExpiringAuthToken, DeleteAuthTokenView
from todos.api.views import TodoViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"todos", TodoViewSet, basename="todo")
urlpatterns = router.urls

urlpatterns += [
    path("auth-token/", ObtainExpiringAuthToken.as_view(), name="auth-token"),
    path("auth-token/delete/", DeleteAuthTokenView.as_view(), name="delete-auth-token"),
]
