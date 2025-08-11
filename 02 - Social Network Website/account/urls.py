from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    path("register/", RegisterView.as_view( ), name="user_register")
]