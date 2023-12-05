from ..serializers.password_reset_serializer import CustomPasswordResetSerializer
from dj_rest_auth.views import PasswordResetView as _PasswordResetView


class PasswordResetView(_PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
