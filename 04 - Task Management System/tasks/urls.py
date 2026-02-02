from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path("dashboard/", TaskDashboardView.as_view(), name="task_dashboard"),
]