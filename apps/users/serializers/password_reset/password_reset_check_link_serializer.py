from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.token_generators import PasswordResetTokenGenerator


class PasswordResetCheckLinkSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):

        try:
            user_id = urlsafe_base64_decode(attrs["user_id"]).decode()
            user = get_user_model().objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise ValidationError({'user_id': ['Invalid value']})

        checker = PasswordResetTokenGenerator().check_token(user, attrs['token'])
        if not checker['status']:
            raise ValidationError({'token': checker['details']})

        return attrs
