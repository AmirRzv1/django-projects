from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),

    path("password-reset/", CostumePasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", CostumePasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CostumePasswordResetConfirm.as_view(), name="password_reset_confirm"),
]