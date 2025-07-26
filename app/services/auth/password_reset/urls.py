from django.urls import path

from . import views

urlpatterns = [
    path(
        "forgot",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
]
