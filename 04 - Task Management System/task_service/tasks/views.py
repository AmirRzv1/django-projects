# Django
import json
from django.http import JsonResponse
from django.views import View
from .models import Task

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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

# ✓ Fixed
class UserTaskCreateAPIView(View):
    def post(self, request):
        # Parse JSON with error handling
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format"},
                status=400
            )

        # Extract fields
        user_id = data.get("user_id")
        title = data.get("title")
        description = data.get("description", "")  # Optional field with default

        # Validate required fields exist
        if not user_id:
            return JsonResponse(
                {"success": False, "error": "user_id is required"},
                status=400
            )

        if not title:
            return JsonResponse(
                {"success": False, "error": "title is required"},
                status=400
            )

        # Validate user_id is a valid integer
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return JsonResponse(
                {"success": False, "error": "user_id must be a valid integer"},
                status=400
            )

        # Create task
        try:
            Task.objects.create(
                owner=user_id,
                title=title,
                description=description
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Task created successfully"
                },
                status=201
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"Failed to create task | {e}"},
                status=500
            )

# ✓ Fixed
class TaskSoftDeleteAPIView(View):
    def post(self, request):
        # Handle JSON parsing errors
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format"},
                status=400
            )

        # Validate task_id exists in request
        task_id = data.get("task_id")
        if not task_id:
            return JsonResponse(
                {"success": False, "error": "task_id is required"},
                status=400
            )

        # Handle task not found
        try:
            real_task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Task not found"},
                status=404
            )

        # ✓ Perform soft delete
        real_task.status = "soft_delete"
        real_task.save()
        return JsonResponse(
            {"success": True, "message": "Task soft-deleted successfully"},
            status=200
        )

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










