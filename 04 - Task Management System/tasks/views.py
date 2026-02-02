from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
class TaskDashboardView(LoginRequiredMixin, View):
    login_url = "accounts:user_login"  # redirect here if not logged in

    def get(self, request):
        return render(request, "tasks/dashboard.html")

class TaskCreateView(View):
    form_class = TasksCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, "tasks/task_create.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Task.objects.create(title=data["title"], description=data["description"], owner=request.user)
            messages.success(request, "Task created Successfully.")
            return redirect("tasks:task_dashboard")
        return render(request, "tasks/dashboard.html", {"form": form})









