from django.urls import path

from . import views

app_name = "session_tokens"

urlpatterns = [
    path("finalize", views.FinalizeAuthView.as_view(), name="finalize"),
    path("authenticate", views.get_scope_permission, name="authenticate"),
]
