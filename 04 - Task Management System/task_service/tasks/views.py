import logging

# Django
from .models import Task

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

logger = logging.getLogger(__name__)

# ✓ DRF Applied
class UserTasksGetAPIView(APIView):

    def get(self, request):
        user_id = request.user.id

        # LOGGING
        logger.info("Fetching tasks", extra={"user_id": user_id})


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

        # LOGGING
        logger.info(
            "Tasks retrieved",
            extra={
                "user_id": user_id,
                "active_count": len(active_tasks),
                "deleted_count": len(deleted_tasks)
            }
        )

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
        # LOGGING
        logger.info("Task creation attempt", extra={"user_id": request.user.id})

        serializer = UserTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            user_id = request.user.id
            title = data["title"]
            description = data["description"]

            task = Task.objects.create(owner=user_id, title=title, description=description)

            # LOGGING
            logger.info(
                "Task created",
                extra={
                    "user_id": user_id,
                    "task_id": task.id,
                    "title": title
                }
            )

            return Response({ "success": True}, status=status.HTTP_201_CREATED)

        # LOGGING
        logger.warning(
            "Task creation failed - validation error",
            extra={
                "user_id": request.user.id,
                "errors": serializer.errors
            }
        )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# ✓ DRF Applied
class TaskSoftDeleteAPIView(APIView):
    def post(self, request, task_id):
        # LOGGING
        logger.info(
            "Task soft delete attempt",
            extra={"user_id": request.user.id, "task_id": task_id}
        )

        try:
            task = Task.objects.get(pk=task_id, owner=request.user.id)
        except Task.DoesNotExist:
            # LOGGING
            logger.warning(
                "Task not found for soft delete",
                extra={"user_id": request.user.id, "task_id": task_id}
            )

            return Response(
                {"success": False, "error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        task.status = "soft_delete"
        task.save()

        # LOGGING
        logger.info(
            "Task soft deleted",
            extra={"user_id": request.user.id, "task_id": task_id}
        )

        return Response({"success": True},
                                status=status.HTTP_200_OK)

# ✓ DRF Applied
class TaskDetailAPIView(APIView):
    def get(self, request, task_id):
        # LOGGING
        logger.info(
            "Task detail request",
            extra={"user_id": request.user.id, "task_id": task_id}
        )
        try:
            task = Task.objects.get(owner=request.user.id, pk=task_id)
        except Task.DoesNotExist:
            # LOGGING
            logger.warning(
                "Task not found",
                extra={"user_id": request.user.id, "task_id": task_id}
            )
            return Response({"success": False, "error": "Task not exist."},
                            status=status.HTTP_404_NOT_FOUND)
        # LOGGING
        logger.info(
            "Task detail retrieved",
            extra={"user_id": request.user.id, "task_id": task_id}
        )
        return Response({"success": True,
                         "title": task.title,
                         "description": task.description,
                         "status": task.status},
                        status=status.HTTP_200_OK)

# ✓ DRF Applied
class TaskRestoreAPIView(APIView):
    def post(self, request, task_id):
        # LOGGING
        logger.info(
            "Task restore attempt",
            extra={"user_id": request.user.id, "task_id": task_id}
        )
        try:
            task = Task.objects.get(owner=request.user.id, pk=task_id)
        except Task.DoesNotExist:
            # LOGGING
            logger.warning(
                "Task not found for restore",
                extra={"user_id": request.user.id, "task_id": task_id}
            )
            return Response({"success": False, "error": "Task not found."},
                            status=status.HTTP_404_NOT_FOUND)

        task.status = "ongoing"
        task.save()

        # LOGGING
        logger.info(
            "Task restored",
            extra={"user_id": request.user.id, "task_id": task_id}
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

# ✓ DRF Applied
class TaskHardDeleteAPIView(APIView):
    def post(self, request, task_id):
        # LOGGING
        logger.info(
            "Task hard delete attempt",
            extra={"user_id": request.user.id, "task_id": task_id}
        )
        try:
            task = Task.objects.get(owner=request.user.id, pk=task_id)
        except Task.DoesNotExist:
            # LOGGING
            logger.warning(
                "Task not found for hard delete",
                extra={"user_id": request.user.id, "task_id": task_id}
            )
            return Response({"success": False, "error": "Task not found."},
                            status=status.HTTP_404_NOT_FOUND)

        task.delete()

        # LOGGING
        logger.info(
            "Task hard deleted",
            extra={"user_id": request.user.id, "task_id": task_id}
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

# ✓ DRF Applied
class TaskUpdateAPIView(APIView):
    def post(self, request, task_id):
        # LOGGING
        logger.info(
            "Task update attempt",
            extra={"user_id": request.user.id, "task_id": task_id}
        )

        serializer = TaskUpdateSerializer(data=request.data)

        if serializer.is_valid():
            try:
                task = Task.objects.get(owner=request.user.id, pk=task_id)
            except Task.DoesNotExist:
                # LOGGING
                logger.warning(
                    "Task not found for update",
                    extra={"user_id": request.user.id, "task_id": task_id}
                )
                return Response({"success": False, "error": "Task does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            task.title = serializer.validated_data["title"]
            task.description = serializer.validated_data["description"]
            task.status = serializer.validated_data["status"]
            task.save()

            # LOGGING
            logger.info(
                "Task updated",
                extra={
                    "user_id": request.user.id,
                    "task_id": task_id,
                    "new_status": task.status
                }
            )

            return Response({"success": True}, status.HTTP_200_OK)

        # LOGGING
        logger.warning(
            "Task update failed - validation error",
            extra={
                "user_id": request.user.id,
                "task_id": task_id,
                "errors": serializer.errors
            }
        )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )













