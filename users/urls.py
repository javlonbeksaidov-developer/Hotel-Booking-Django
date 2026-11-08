from django.urls import path

from .auth import login_page, logout_page, profile_page, register_page

app_name = "users"

urlpatterns = [
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("register/", register_page, name="register"),
    path("profile/", profile_page, name="profile"),
]
