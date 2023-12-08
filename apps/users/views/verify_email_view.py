from dj_rest_auth.registration.views import VerifyEmailView as _VerifyEmailView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status


class VerifyEmailView(_VerifyEmailView):
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        if resp.data == {'detail': 'ok'}:
            email_address = self.get_object().email_address
            user = get_user_model().objects.filter(email=email_address).first()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )


