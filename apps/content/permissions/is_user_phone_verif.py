from rest_framework.permissions import BasePermission

from apps.users.models import UserProfile


class IsUserPhoneVerif(BasePermission):
    message = "Написання постів доступне лише користувачам з верифікованим номером телефону"

    def has_permission(self, request, view):
        user = request.user

        if not UserProfile.objects.filter(user=user).exists():
            self.message = "User profile with such user does not exist"
            return False

        return request.user.is_authenticated and request.user.userprofile.phone_verified
