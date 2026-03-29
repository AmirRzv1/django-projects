from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    # No changes for DRF
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("task_create/", UserTaskCreateView.as_view(), name="task_create"),
    path("task-soft-delete/<int:task_id>", TaskSoftDelete.as_view(), name="task_soft_delete"),
    path("task-update/<int:task_id>", TaskUpdateView.as_view(), name="task_update"),
    path("recycle-bin/", RecycleBinView.as_view(), name="recycle_bin"),
    path("restore-task/<int:task_id>/", TaskRestoreView.as_view(), name="task_restore"),
    path("task-hard-delete/<int:task_id>/", TaskHardDeleteView.as_view(), name="task_hard_delete")
]