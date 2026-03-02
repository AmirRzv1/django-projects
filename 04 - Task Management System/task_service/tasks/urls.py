from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path("tasks/", UserTasksGetAPIView.as_view(), name="user_task"),
    path("task_create/", UserTaskCreateAPIView.as_view(), name="task_create"),
]