import json

# Django
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

# just disable the csrf for whole views in the project to pass it
# because im using it as only internall api calling it doesnt render
# anything so isntead of didsable the csrf for each view i disable it globally

# ✓ Fixed
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

# ✓ Converted to DRF
class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "User created successfully.",},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# ✓ Fixed
class UserInformationAPIView(View):
    def get(self, request):
        data = json.loads(request.body)

        if not data:
            return JsonResponse({"success": False, "msg": "Empty request."})


        # Handle user not found
        try:
            user = User.objects.get(pk = data["user_id"])
        except User.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "User not found"},
                status=404
            )

        return JsonResponse({"success": True,
                             "username": user.username,
                             "email": user.email})






