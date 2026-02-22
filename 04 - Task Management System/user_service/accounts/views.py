import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError


@method_decorator(csrf_exempt, name="dispatch")
class UserLoginAPIView(View):
    # check that if the user is sending the username or email
    # based on that we return the related information
    def validate_username_or_email(self, data):
        if data and "@" in data:
            return {"email": data.lower()}
        else:
            return {"username": data.lower()}


    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data["username"]
            password = data["password"]
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"success": False, "error": "Invalid request body"}, status=400)

        result = self.validate_username_or_email(username)

        if result.get("username", None):
            user = authenticate(username=result["username"], password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True, "user_id": user.id, "username": user.username})

        else:
            user = authenticate(username=result["username"], password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True, "user_id": user.id, "username": user.username})

        return JsonResponse({"success": False, "error": "Invalid username or password"}, status=401)

@method_decorator(csrf_exempt, name="dispatch")
class UserLogoutAPIView(View):
    def post(self, request):
        data = json.loads(request.body)
        print("data =", data)
        user_id = data.get("user_id")
        if not user_id:
            return JsonResponse({"success": False, "error": "No user exists."}, status=400)

        real_user = User.objects.get(id=user_id)
        print("real_user = ", real_user)
        if real_user:
            logout(request)
            return JsonResponse({"success": True})

@method_decorator(csrf_exempt, name="dispatch")
class UserRegisterAPIView(View):
    def post(self, request):

        # Handle invalid JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON."},
                status=400
            )

        if not data:
            return JsonResponse(
                {"success": False, "error": "Data is empty."},
                status=400
            )

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Validate required fields
        if not all([username, email, password]):
            return JsonResponse(
                {"success": False, "error": "All fields are required."},
                status=400
            )

        # Try to create user
        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        except IntegrityError:
            return JsonResponse(
                {"success": False, "error": "Username already exists."},
                status=400
            )
        except DatabaseError:
            return JsonResponse(
                {"success": False, "error": "Database error."},
                status=500
            )

        return JsonResponse(
            {"success": True},
            status=201
        )






