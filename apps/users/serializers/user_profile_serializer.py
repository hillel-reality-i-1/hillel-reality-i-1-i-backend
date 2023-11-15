from rest_framework import serializers
from apps.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_email(self, obj):
        return obj.user.email
