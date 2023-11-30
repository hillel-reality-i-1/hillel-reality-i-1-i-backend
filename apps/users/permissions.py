from rest_framework import permissions


class IsAdminOrProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        return view.kwargs.get("pk") == str(user.userprofile.id)


class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        return view.kwargs.get("pk") == str(user.id)