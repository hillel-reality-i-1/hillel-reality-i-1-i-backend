from rest_framework.permissions import BasePermission


class IsVerifiedAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.author == request.user

    def has_permission(self, request, view):
        return (
            request.method == 'POST' and request.user.is_authenticated and request.user.is_verified()
            or
            request.method in ['GET', 'HEAD', 'OPTIONS']
        )
