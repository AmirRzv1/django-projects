import json
import logging

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

logger = logging.getLogger(__name__)

# ✓ DRF Applied
class UserLoginAPIView(APIView):
    """
    use the credentials to validate the user by email or username
    then create a JWT token and send back the whole result.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        # LOGGING
        logger.info("Login attempt", extra={"username": request.data.get("username", "N/A")})

        # validate the data
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # extract validated user
            user = serializer.validated_data["user"]
            # create a token
            token = generate_jwt_token(user)

            # LOGGING
            logger.info("Login successful", extra={"user_id": user.id, "username": user.username})


            # return the result
            return Response({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        # LOGGING
        logger.warning("Login failed - invalid credentials", extra={"errors": serializer.errors})

        return Response({
            'error': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

# ✓ DRF Applied
class UserRegisterAPIView(APIView):
    """
    Take the username, password and email(optional) and validate it,
    after that save the user and send a message to the web_service.

    """
    permission_classes = [AllowAny]

    def post(self, request):
        # LOGGING
        logger.info("Registration attempt", extra={"username": request.data.get("username", "N/A")})

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # LOGGING
            logger.info("Registration successful", extra={"username": request.data.get("username")})

            return Response(
                {"success": True, "message": "User created successfully.",},
                status=status.HTTP_201_CREATED
            )

        # LOGGING
        logger.warning("Registration failed - validation error", extra={"errors": serializer.errors})

        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# ✓ Fixed | don't need it yet
class UserInformationAPIView(APIView):
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






