import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError

# just disable the csrf for whole views in the project to pass it
# because im using it as only internall api calling it doesnt render
# anything so isntead of didsable the csrf for each view i disable it globally

class UserLoginAPIView(View):
    # check that if the user is sending the username or email
    # based on that we return the related information
    def validate_username_or_email(self, data):
        if data and "@" in data:
            return {"email": data.lower()}
        return {"username": data.lower()}

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid request body"}, status=400)

        username = data["username"]
        password = data["password"]

        if not username or not password:
            return JsonResponse({"success": False, "error": "Username and password are required"}, status=401)

        result = self.validate_username_or_email(username)

        try:
            if "username" in result:
                real_user = User.objects.get(username=username)
                user = authenticate(username=result["username"], password=password)
                if user is None:
                    return JsonResponse({"success": False, "error": "Invalid username or password"},
                                         status=401)
                return JsonResponse({"success": True,
                                     "username": real_user.username,
                                     "user_id": real_user.pk}, status=200)

            else:
                try:
                    user_by_email = User.objects.get(email=result["email"])
                except User.DoesNotExist:
                    return JsonResponse({"success": False, "error": "Invalid username or password"},
                    status = 401)

                user = authenticate(username=user_by_email.username, password=password)
                if user is None:
                    return JsonResponse({"success": False, "error": "Invalid username or password"},
                                         status=401)

                return JsonResponse( {"success": True,
                                  "username": user_by_email.username,
                                  "user_id": user_by_email.pk}, status=200)
        except Exception:
            # Unexpected server/database error
            return JsonResponse(
                {"success": False, "error": "Internal server error"},
                status=500
                    )

        return JsonResponse({"success": False, "error": "Invalid username or password"}, status=401)

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

class UserInformationAPIView(View):
    def get(self, request):
        data = json.loads(request.body)

        if not data:
            return JsonResponse({"success": False, "msg": "Empty request."})

        user = User.objects.get(pk=data["user_id"])
        return JsonResponse({"success": True,
                             "username": user.username,
                             "email": user.email})






