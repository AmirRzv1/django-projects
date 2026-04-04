from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path("tasks/", UserTasksGetAPIView.as_view(), name="user_task"),
    path("task_create/", TaskCreateAPIView.as_view(), name="task_create"),
    path("task-soft-delete/<int:task_id>/", TaskSoftDeleteAPIView.as_view(), name="task_soft_delete"),
    path("task-detail/<int:task_id>/", TaskDetailAPIView.as_view(), name="task_detail"),
    path("task-restore/", TaskRestoreAPIView.as_view(), name="task_restore"),
    path("task-hard-delete/", TaskHardDeleteAPIView.as_view(), name="task_hard_delete"),
    path("task-update/<int:task_id>/", TaskUpdateAPIView.as_view(), name="task_update"),
]