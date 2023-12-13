from rest_framework import permissions

from apps.users.models import UserProfile


class IsVerifiedUser(permissions.BasePermission):
    message = "This content is for verified users only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified()


class IsAdminOrProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        is_userprofile = UserProfile.objects.filter(user=user).exists()

        if is_userprofile:
            userprofile = UserProfile.objects.get(user=user)
            return view.kwargs.get("pk") == str(userprofile.id)
        else:
            return False


class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        return view.kwargs.get("pk") == str(user.id)
