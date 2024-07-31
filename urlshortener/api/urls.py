from django.urls import include, path

urlpatterns = [
    path("auth/", include(("urlshortener.authentication.urls", "authentication"))),
    path("users/", include(("urlshortener.users.urls", "users"))),
]
