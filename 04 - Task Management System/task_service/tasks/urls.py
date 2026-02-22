from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]