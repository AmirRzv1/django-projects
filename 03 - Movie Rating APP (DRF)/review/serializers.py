from rest_framework import serializers

class ReviewCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    movie = serializers.CharField()
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