from rest_framework.permissions import AllowAny

from dj_rest_auth.registration.views import RegisterView

from apps.users.models import User
from apps.users.serializers.custom_registration_serializer import CustomRegistrationSerializer
from django.utils.translation import gettext_lazy as _
from allauth.account import app_settings as allauth_account_settings


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegistrationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_response_data(self, user):
        if allauth_account_settings.EMAIL_VERIFICATION == allauth_account_settings.EmailVerificationMethod.MANDATORY:
            return {"email": _(f"{user.email}"), "id": user.pk}

        super().get_response_data(user)
