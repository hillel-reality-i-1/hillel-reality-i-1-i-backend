from allauth.account.models import EmailConfirmationHMAC, EmailAddress
from django.contrib.auth import get_user_model

from allauth.account.views import ConfirmEmailView

from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from django.core import signing
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import MethodNotAllowed, ValidationError

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from allauth.account import app_settings


class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.kwargs['key'] = serializer.validated_data['key']
        self.object = confirmation = self.get_object()

        email_address = confirmation.confirm(self.request)
        user = get_user_model().objects.filter(email=email_address).first()
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)

    def get_object(self):
        key = self.kwargs["key"]
        emailconfirmation = self.custom_realization_of_emailconfirmationhmac_method_from_key(key)
        return emailconfirmation

    @staticmethod
    def custom_realization_of_emailconfirmationhmac_method_from_key(key):
        try:
            max_age = 60 * 60 * 24 * app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
            pk = signing.loads(key, max_age=max_age, salt=app_settings.SALT)
            ret = EmailConfirmationHMAC(EmailAddress.objects.get(pk=pk, verified=False))
        except signing.SignatureExpired:
            ValidationError({'details': 'signature expired'}, status=status.HTTP_400_BAD_REQUEST)
        except signing.BadSignature:
            ValidationError({'details': 'bad signature'}, status=status.HTTP_400_BAD_REQUEST)
        except EmailAddress.DoesNotExist:
            ValidationError({'details': 'email address does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return ret
