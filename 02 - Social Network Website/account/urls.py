from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    path("register/", UserRegisterView.as_view( ), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="us er_profile"),
    path("reset/", UserPasswordResetView.as_view(), name="reset_password"),
    path("reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),

]