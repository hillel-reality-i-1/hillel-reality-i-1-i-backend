from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.token_generators import PasswordResetTokenGenerator


class PasswordResetCheckLinkSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):

        try:
            uid = urlsafe_base64_decode(attrs["uid"]).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        checker = PasswordResetTokenGenerator().check_token(user, attrs['token'])
        if not checker['status']:
            raise ValidationError({'token': checker['details']})

        return attrs
