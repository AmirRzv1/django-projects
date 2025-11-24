from rest_framework import serializers

class AccountCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)

class AccountShowAllSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
