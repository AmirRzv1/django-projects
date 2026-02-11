from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
class TaskDashboardView(LoginRequiredMixin, View):
    login_url = "accounts:user_login"  # redirect here if not logged in

    def get(self, request):
        # query to get the tasks
        # + exclude -> miad va on mored ro ignore mikone
        task_get_query = Task.objects.filter(owner=request.user).exclude(status="soft_delete")
        # validate the status to be correct
        task_status = request.GET.get("status")
        # no status so we send the related ones for the same user
        if not task_status:
            print(task_get_query.count(), task_get_query)
            return render(request, "tasks/dashboard.html", {"tasks": task_get_query})
        # if it was not in the status we send an error
        elif task_status not in [state[0] for state in Task.STATUS_CHOICES]:
            messages.error(request, "Wrong status is given !")
            return redirect("tasks:dashboard")

        # we send related ones with the related status
        tasks = task_get_query.filter(status=task_status)

        return render(request, "tasks/dashboard.html", {"tasks": tasks})

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
        task = get_object_or_404(Task, owner=request.user, pk=task_id)
        task.status = "soft_delete"
        task.save()

        messages.success(request, "Task soft deleted successfully!")
        return redirect("tasks:task_dashboard")


class RecycleBinView(View):
    def get(self, request):
        soft_deleted_tasks = Task.objects.filter(owner=request.user, status="soft_delete")
        return render(request, "tasks/recycle_bin.html", {"tasks": soft_deleted_tasks})

class TaskRestoreView(View):
    def post(self, request, task_id):
        task = Task.objects.get(owner=request.user, pk=task_id)
        if task:
            task.status = "ongoing"
            task.save()

            messages.success(request, "Task restored successfully.")
            return redirect("tasks:recycle_bin")

        messages.error(request, "No Task with this id.")
        return redirect("tasks:recycle_bin")








