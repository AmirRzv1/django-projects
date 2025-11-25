from rest_framework import serializers

class ReviewCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    movie = serializers.CharField()
    rate = serializers.IntegerField()
    comment = serializers.CharField()