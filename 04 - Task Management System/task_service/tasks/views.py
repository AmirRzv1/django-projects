# Django
import json
from django.http import JsonResponse
from django.views import View
from .models import Task

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# ✓ DRF Applied
class UserTasksGetAPIView(APIView):

    def get(self, request):
        user_id = request.user.id

        all_tasks = Task.objects.filter(owner=user_id).values(
            'id', 'title', 'description', 'status', 'created_at'
        )

        active_tasks = []
        deleted_tasks = []

        for task in all_tasks:
            if task['status'] == 'soft_delete':
                deleted_tasks.append(task)
            else:
                active_tasks.append(task)

        return Response({
            "active_tasks": active_tasks,
            "active_count": len(active_tasks),
            "deleted_tasks": deleted_tasks,
            "deleted_count": len(deleted_tasks),
        }, status=status.HTTP_200_OK)

# ✓ DRF Applied
class TaskCreateAPIView(APIView):
    """
    take the data from serializer and extract it and if it is True
    we will create the task for that specific user.
    """
    def post(self, request):
        serializer = UserTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            user_id = request.user.id
            title = data["title"]
            description = data["description"]

            Task.objects.create(owner=user_id, title=title, description=description)

            return Response({ "success": True}, status=status.HTTP_201_CREATED)

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# ✓ DRF Applied
class TaskSoftDeleteAPIView(APIView):
    def post(self, request, task_id):
            try:
                task = Task.objects.get(pk=task_id, owner=request.user.id)
            except Task.DoesNotExist:
                return Response(
                    {"success": False, "error": "Task not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            task.status = "soft_delete"
            task.save()

            return Response({"success": True},
                                status=status.HTTP_200_OK)

# ✓ Fixed
class TaskDetailAPIView(View):
    def get(self, request):
        # Handle JSON parsing errors
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format"},
                status=400
            )

        task_id = data.get("task_id")
        user_id = data.get("user_id")
        # Validate required parameters
        if not task_id:
            return JsonResponse(
                {"success": False, "error": "task_id is required"},
                status=400
            )

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "user_id is required"},
                status=400
            )

        try:
            # tip : JsonResponse cant send the django object because it cant convert it
            # instead for easy part we can use .values() on our query.
            task = Task.objects.filter(pk=task_id, owner=user_id).values().first()
            return JsonResponse( {"success": True, "task": task } )
        except Exception as e:
            print(e)
            return JsonResponse( {"success": False, "error": str(e)})

# ✓ Fixed
class TaskRestoreAPIView(View):
    def post(self, request):
        # Handle JSON parsing errors
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format"},
                status=400
            )

        # Validate required fields
        task_id = data.get("task_id")
        user_id = data.get("user_id")

        if not task_id:
            return JsonResponse(
                {"success": False, "error": "task_id is required"},
                status=400
            )

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "user_id is required"},
                status=400
            )

        # Handle task not found or access denied
        try:
            real_task = Task.objects.get(pk=task_id, owner=user_id)
        except Task.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Task not found or access denied"},
                status=404
            )

        # Check if task is actually soft-deleted
        if real_task.status != "soft_delete":
            return JsonResponse(
                {"success": False, "error": "Task is not deleted"},
                status=400
            )

        # Restore task
        real_task.status = "ongoing"
        real_task.save()

        return JsonResponse(
            {"success": True, "message": "Task restored successfully"},
            status=200
        )

# ✓ Fixed
class TaskHardDeleteAPIView(View):
    def post(self, request):
        # Handle JSON parsing errors
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format"},
                status=400
            )

        # Validate required fields
        task_id = data.get("task_id")
        user_id = data.get("user_id")

        if not task_id:
            return JsonResponse(
                {"success": False, "error": "task_id is required"},
                status=400
            )

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "user_id is required"},
                status=400
            )

        # Handle task not found or access denied
        try:
            task = Task.objects.get(pk=task_id, owner=user_id)
        except Task.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Task not found or access denied"},
                status=404
            )

        # Safety check: only hard-delete if already soft-deleted
        if task.status != "soft_delete":
            return JsonResponse(
                {"success": False, "error": "Task must be soft-deleted first"},
                status=400
            )

        # Perform hard delete
        task.delete()

        return JsonResponse(
            {"success": True, "message": "Task permanently deleted"},
            status=200
        )

# ✓ Fixed
class TaskUpdateAPIView(View):
    def post(self, request):
        # Handle JSON parsing errors
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format"},
                status=400
            )

        # Validate required fields
        task_id = data.get("task_id")
        user_id = data.get("user_id")

        if not task_id:
            return JsonResponse(
                {"success": False, "error": "task_id is required"},
                status=400
            )

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "user_id is required"},
                status=400
            )

        # Handle task not found or access denied
        try:
            task = Task.objects.get(pk=task_id, owner=user_id)
        except Task.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Task not found or access denied"},
                status=404
            )

        # Check if task is soft-deleted
        if task.status == "soft_delete":
            return JsonResponse(
                {"success": False, "error": "Cannot update deleted task"},
                status=400
            )

        # Only update fields that are provided (partial update)
        title = data.get("title")
        description = data.get("description")
        status = data.get("status")

        task.title = title
        task.description = description
        task.status = status

        task.save()

        return JsonResponse(
            {"success": True, "message": "Task updated successfully"},
            status=200
        )










