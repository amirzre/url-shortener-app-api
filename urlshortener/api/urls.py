from django.urls import include, path

urlpatterns = [
    path("auth/", include(("urlshortener.authentication.urls", "authentication"))),
    path("users/", include(("urlshortener.users.urls", "users"))),
    path("errors/", include(("urlshortener.errors.urls", "errors"))),
    path("files/", include(("urlshortener.files.urls", "files"))),
    path(
        "google-oauth2/", include(("urlshortener.blog_examples.google_login_server_flow.urls", "google-oauth2"))
    ),
]
