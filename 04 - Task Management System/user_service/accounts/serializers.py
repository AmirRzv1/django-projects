from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

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

class UserLoginSerializer(serializers.Serializer):
    # our front-end or web_service, sends these fields as json
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # overwrite the validate method to implement the logic of logging in
    # user with email or username.
    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        user = None
        if "@" in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")

        else:
            username = username_or_email

        # Tip : authenticate, validate users only with the username.
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Tip : serializers must return data so we use it in our view
        # whatever we return becomes serializer.validated_data
        data['user'] = user
        return data









