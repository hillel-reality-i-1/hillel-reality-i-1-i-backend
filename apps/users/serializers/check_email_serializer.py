from rest_framework import serializers


class UserCheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
