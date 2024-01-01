import django.contrib.auth.views
from django.urls import path, reverse_lazy

import users.views

app_name = "users"

urlpatterns = [
    path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    path(
        "password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change_done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "signup/",
        users.views.sign_up,
        name="signup",
    ),
    path(
        "activate/<str:username>/",
        users.views.activate,
        name="activate",
    ),
    path(
        "profile/<int:profile_id>",
        users.views.profile_by_id,
        name="profile_by_id",
    ),
    path(
        "profile/",
        users.views.user_profile,
        name="user_profile",
    ),
]
