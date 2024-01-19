from dj_rest_auth.views import PasswordResetView as _PasswordResetView
from apps.users.serializers import CustomPasswordResetSerializer


class PasswordResetView(_PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
