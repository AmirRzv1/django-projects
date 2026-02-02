from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class TaskDashboardView(LoginRequiredMixin, View):
    login_url = "accounts:user_login"  # redirect here if not logged in

    def get(self, request):
        return render(request, "tasks/dashboard.html")

class TaskCreateView(View):
    def get(self, request):
        return render(request, "tasks/task_create.html")