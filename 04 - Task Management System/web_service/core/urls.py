from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("task_create/", UserTaskCreateView.as_view(), name="task_create"),

]