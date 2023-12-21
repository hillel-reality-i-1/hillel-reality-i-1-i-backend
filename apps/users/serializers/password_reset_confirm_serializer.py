from dj_rest_auth.serializers import PasswordResetConfirmSerializer as _PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PasswordResetConfirmSerializer(_PasswordResetConfirmSerializer):

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = urlsafe_base64_decode(attrs["uid"]).decode()
            self.user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        print(default_token_generator)

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs
