from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "groups",
            "user_permissions",
        )
