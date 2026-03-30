from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    # + write_only means : accept in post - never returns it
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

        extra_kwargs = {
            "email": {"required": False, "allow_blank": True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)