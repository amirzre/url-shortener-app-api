from django.urls import path

from .apis import ShortenerDetailApi, ShortenerListApi

urlpatterns = [
    path("", ShortenerListApi.as_view(), name="detail"),
    path("create/", ShortenerDetailApi.as_view(), name="create"),
]
