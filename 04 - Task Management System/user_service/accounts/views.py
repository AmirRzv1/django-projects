import json

# jwt
from .utils import generate_jwt_token

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
from rest_framework.permissions import AllowAny
from .serializers import *

# just disable the csrf for whole views in the project to pass it
# because im using it as only internall api calling it doesnt render
# anything so isntead of didsable the csrf for each view i disable it globally

# ✓ Fixed
class UserLoginAPIView(APIView):
    """
    use the credentials to validate the user by email or username
    then create a JWT token and send back the whole result.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # validate the data
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # extract validated user
            user = serializer.validated_data["user"]
            # create a token
            token = generate_jwt_token(user)

            # return the result
            return Response({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'error': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

# ✓ DRF applied
class UserRegisterAPIView(APIView):
    """
    Take the username, password and email(optional) and validate it,
    after that save the user and send a message to the web_service.

    """
    permission_classes = [AllowAny]

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






