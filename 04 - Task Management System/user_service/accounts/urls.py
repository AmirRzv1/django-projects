from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    # path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),
    path("register/", UserRegisterAPIView.as_view(), name="user_register"),

    # dont need it yet.
    path("information/", UserInformationAPIView.as_view(), name="user_information"),
]