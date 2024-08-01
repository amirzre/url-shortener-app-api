from django.urls import path

from .apis import RedirectShortURLView, ShortenerDetailApi

urlpatterns = [
    path("create/", ShortenerDetailApi.as_view(), name="create_short_url"),
    path("<str:short_url>/", RedirectShortURLView.as_view(), name="redirect_short_url"),
]
