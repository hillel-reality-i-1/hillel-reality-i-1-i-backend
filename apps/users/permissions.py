from rest_framework import permissions, status
from rest_framework.response import Response

from apps.files.models import Image, File
from apps.users.models import UserProfile, UserProfileExtended, User


class IsVerifiedUser(permissions.BasePermission):
    message = "This content is for verified users only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified()


class IsAdminOrImageOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        is_image_exist = Image.objects.filter(author=user).exists()

        if is_image_exist:
            image = Image.objects.get(author=user)
            return view.kwargs.get("pk") == str(image.id)
        else:
            return False


class IsAdminOrPortfolioOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        is_portfolio_ext = File.objects.filter(author=user).exists()

        if is_portfolio_ext:
            portfolio_ext = File.objects.filter(author=user, pk=view.kwargs.get("pk")).first()
            return bool(portfolio_ext)
        else:
            return False


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


class IsAdminOrProfileExtendedOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        is_userprofile_ext = UserProfileExtended.objects.filter(user=user).exists()

        if is_userprofile_ext:
            userprofile_ext = UserProfileExtended.objects.get(user=user)
            return view.kwargs.get("pk") == str(userprofile_ext.id)


class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        return view.kwargs.get("pk") == str(user.id)


class IsAdminOrUserProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        requested_user = User.objects.filter(id=view.kwargs.get("user_id")).first()
        if not requested_user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if UserProfile.objects.filter(user=requested_user).exists():
            user_profile = UserProfile.objects.get(user=requested_user)
            return user_profile.user.id == user.id
        else:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class IsAdminOrAvatarOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        requested_user = User.objects.filter(id=view.kwargs.get("user_id")).first()
        if not requested_user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if Image.objects.filter(author=requested_user).exists():
            image = Image.objects.get(author=requested_user)
            return user.id == image.author.id
        else:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class IsAdminOrExpertUserProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        requested_user = User.objects.filter(id=view.kwargs.get("user_id")).first()
        if not requested_user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if UserProfileExtended.objects.filter(user=requested_user).exists():
            user_profile_ext = UserProfileExtended.objects.get(user=requested_user)
            return user_profile_ext.user.id == user.id
        else:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
