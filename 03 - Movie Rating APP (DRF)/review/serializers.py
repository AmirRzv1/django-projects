from rest_framework import serializers
from .models import Movie
from django.contrib.auth.models import User

class ReviewCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # we need the actual movie object related to the id that
    # we have from our user so we use this and we set queryset
    # so it has control over all the objects and checks them all
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    rate = serializers.IntegerField()
    comment = serializers.CharField()

class MovieCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    director = serializers.CharField()
    category = serializers.CharField()

class MovieShowAllSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    director = serializers.CharField()
    category = serializers.CharField()