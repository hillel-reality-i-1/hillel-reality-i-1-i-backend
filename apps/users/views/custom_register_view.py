from rest_framework.permissions import AllowAny

from dj_rest_auth.registration.views import RegisterView

from apps.users.models import User
from apps.users.serializers.custom_registration_serializer import CustomRegistrationSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegistrationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
