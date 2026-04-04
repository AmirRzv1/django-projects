from rest_framework import serializers

class UserTaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255,
                                        allow_null=True,
                                        allow_blank=True,
                                        required=False,
                                        default="")