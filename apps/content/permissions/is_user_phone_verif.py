from rest_framework.permissions import BasePermission


class IsUserPhoneVerif(BasePermission):
    message = "Написання постів доступне лише користувачам з верифікованим номером телефону"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.phone_verified
