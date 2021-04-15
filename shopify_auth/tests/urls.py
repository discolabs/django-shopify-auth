from django.urls import include, path

urlpatterns = [
    path("", include("shopify_auth.urls")),
    path("session_tokens/", include("shopify_auth.session_tokens.urls", namespace="session_tokens")),
]
