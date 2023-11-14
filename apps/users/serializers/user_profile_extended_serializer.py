from rest_framework import serializers
from apps.users.models import UserProfileExtended


class UserProfileExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileExtended
        fields = "__all__"
