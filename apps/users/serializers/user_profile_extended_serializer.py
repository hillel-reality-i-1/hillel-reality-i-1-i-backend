from rest_framework import serializers
from apps.users.models import UserProfileExtended


class UserProfileExtendedSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileExtended
        fields = "__all__"

    def get_email(self, obj):
        return obj.user.email
