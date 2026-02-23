import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Task

# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class UserTasksGetAPIView(View):
    def get(self, request):
        data = json.loads(request.body)
        user_id = data.get("user_id")
        tasks = Task.objects.filter(owner=user_id)
        return JsonResponse( {"success": True,
                              "tasks": tasks} )

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








