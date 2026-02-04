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

class TaskUpdateView(View):
    form_class = TaskUpdateForm

    # We need to use ModelForm so we can use the instance to pre-fill
    # the data for our forms in the templates.
    def get(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        form = self.form_class(instance=task)
        return render(request, "tasks/task_update.html", {"form": form})

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Updated Successfully!")
            return redirect("tasks:task_dashboard")
        return render(request, "tasks/task_update.html", {"form": form})

class TaskDeleteView(View):
    def get(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect("tasks:task_dashboard")









