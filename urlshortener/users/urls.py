from django.urls import path

from .apis import UserCreateApi

urlpatterns = [
    path("create/", UserCreateApi.as_view(), name="create"),
]
