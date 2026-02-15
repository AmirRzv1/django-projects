from django.urls import path
from views import *

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),

    path("password-reset/", CostumePasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),

    path("password-reset/done/", CostumePasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/", CostumePasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path("reset/done/", CostumePasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),

]