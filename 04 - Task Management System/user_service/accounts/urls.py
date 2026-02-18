from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),
]