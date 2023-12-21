from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "email",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "username_changed",
            "is_deleted_user",
            "date_joined",
            "groups",
            "user_permissions",
            "last_full_name_change",
        )
