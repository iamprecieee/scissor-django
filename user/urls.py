from django.urls import path
from .views import register_user, login_user, edit_password
from django.contrib.auth.views import LogoutView


app_name = "user"

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit-password/", edit_password, name="edit-password"),
]
