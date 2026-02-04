from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path("dashboard/", TaskDashboardView.as_view(), name="task_dashboard"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
    path("update/<int:task_id>/", TaskUpdateView.as_view(), name="task_update")
]