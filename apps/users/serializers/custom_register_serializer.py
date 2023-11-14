from rest_framework import serializers
from apps.users.models import User


class CustomRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}, "last_name": {"required": False}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
