from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class AccountCreateView(APIView):
    # i defined a permission for this view so only authenticated users
    # can use this
    permission_classes = [IsAuthenticated]

    # set the permission only for get method and not the entire
    # class so only get now have the permission and post is AllowAny
    def get_permissions(self):
        if self.request.method == "GET":
            # we instantiate the permission class because in a method
            # DRF can't do this for use we need to do it manually.
            return [IsAuthenticated()]
        return []


    def get(self, request):
        data = User.objects.all()
        print(data)
        serialized_data = AccountShowAllSerializer(instance=data, many=True)
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)



    def post(self, request):
        serialized_data = AccountCreateSerializer(data=request.data)

        if serialized_data.is_valid():
            validated_data = serialized_data.validated_data
            user = User.objects.create_user(username=validated_data["email"], **validated_data)
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
