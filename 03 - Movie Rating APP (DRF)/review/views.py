from django.shortcuts import render
from django.template.defaulttags import comment
from rest_framework import views
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class MovieCreateView(views.APIView):
    def get(self, request):
        data = Movie.objects.all()
        serialized_data = MovieShowAllSerializer(instance=data, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


    def post(self, request):
        serialized_data = MovieCreateSerializer(data=request.data)
        if serialized_data.is_valid():
            validated_data = serialized_data.validated_data
            movie = Movie.objects.create(**validated_data)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)



class ReviewCreateView(views.APIView):
    def post(self, request):
        serialized_data = ReviewCreateSerializer(data=request.data)

        if serialized_data.is_valid():
            data = serialized_data.validated_data
            review = Review.objects.create(**data)
            return Response(data=serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


