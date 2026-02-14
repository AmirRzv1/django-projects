from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView
from django.contrib.auth import views

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),

    path("password-reset/", views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),

    path("password-reset/done/", views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path("reset/done/", views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),

]