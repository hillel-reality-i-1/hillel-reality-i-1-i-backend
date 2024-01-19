from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from dj_rest_auth.views import PasswordResetConfirmView as _PasswordResetConfirmView
from apps.users.serializers import PasswordResetConfirmSerializer


class PasswordResetConfirmView(_PasswordResetConfirmView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        uid = urlsafe_base64_decode(serializer["uid"].value).decode()
        user = get_user_model().objects.get(pk=uid)

        get_adapter().send_reset_password_confirm_success_mail(user)
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'detail': _('Password has been reset with the new password.'),
                'token': token.key,
            },
        )
