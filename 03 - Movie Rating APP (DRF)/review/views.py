from django.shortcuts import render
from rest_framework import views
from .serializers import *
from .models import Review
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ReviewCreateView(views.APIView):
    def post(self, request):
        serialized_data = ReviewCreateSerializer(data=request.data)

        if serialized_data.is_valid():
            data = serialized_data.validated_data
            review = Review.objects.create(**data)
            return Response(data=review, status=status.HTTP_201_CREATED)
        return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


