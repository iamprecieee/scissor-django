from django.urls import path
from .views import (register_user, login_user, edit_password, password_reset_request,
                     password_reset_confirm)
from django.contrib.auth.views import LogoutView


app_name = "user"

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit-password/", edit_password, name="edit-password"),
    path("password-reset-request/", password_reset_request, name="password-reset-request"),
    path("reset-password/<uidb64>/<token>/", password_reset_confirm, name="password-reset-confirm"),
    # path("password-change/", set_new_password, name="password-change"),
]
