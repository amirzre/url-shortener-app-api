from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .apis import UserMeApi

urlpatterns = [
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", TokenObtainPairView.as_view(), name="login"),
                    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
                    path("verify/", TokenVerifyView.as_view(), name="verify"),
                ],
                "jwt",
            )
        ),
    ),
    path("me/", UserMeApi.as_view(), name="me"),
]
