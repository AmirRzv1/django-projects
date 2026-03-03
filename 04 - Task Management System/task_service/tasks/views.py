import json
from django.http import JsonResponse
from django.views import View
from .models import Task

# Create your views here.
class UserTasksGetAPIView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid request body"},status=400)

        user_id = data.get("user_id")
        if not user_id:
            return JsonResponse({"success": False, "error": "Missing user_id"},status=400)

        tasks_query = Task.objects.filter(owner=user_id)
        tasks = list(tasks_query.values())

        return JsonResponse(
            {
                "success": True,
                "tasks": tasks
            },
            status=200)

class UserTaskCreateAPIView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get("user_id")
        title = data.get("title")
        description = data.get("description")
        try:
            Task.objects.create(owner=user_id, title=title, description=description)
            return JsonResponse({
                "success": True,
            })
        except Exception:
            return JsonResponse( {
                "success": False
            } )

# need adjustment
class TaskSoftDeleteAPIView(View):

    def post(self, request):
        data = json.loads(request.body)
        if not data:
            return JsonResponse( {"success": False, "error": "Empty data !"} )

        task_id = data.get("task_id")
        real_task = Task.objects.get(pk=task_id)
        real_task.status = "soft_delete"
        real_task.save()
        return JsonResponse( {"success": True, } )

class TaskDetailAPIView(View):
    def get(self, request):
        data = json.loads(request.body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        try:
            task = Task.objects.filter(pk=task_id, owner=user_id)
            task = task.first()
            return JsonResponse( {"success": True, "task": task } )
        except Exception as e:
            return JsonResponse( {"success": False, "error": e})

class TaskRestoreAPIView(View):
    def post(self, request):
        pass




