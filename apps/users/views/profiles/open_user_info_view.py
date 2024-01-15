from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.files.models import File
from apps.users.models import User


class UserOpenInfoView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def _get_user_info_or_404(self, user_id):
        return get_object_or_404(
            User.objects.select_related(
                "userprofile",
                "userprofileextended",
                "userprofile__country",
                "userprofile__city",
                "userprofile__profile_picture",
                "userprofileextended__profession",
                "userprofileextended__service",
            ).prefetch_related(Prefetch("file_set", queryset=File.objects.all(), to_attr="user_files")),
            id=user_id,
        )

    def _get_user_profile_dict(self, user_profile):
        keys = [
            "about_my_self",
            "country",
            "city",
            "profile_picture",
        ]
        if user_profile.phone_is_visible:
            keys.append("phone_number")
        if user_profile.telegram_is_visible:
            keys.append("telegram")
        if user_profile.instagram_is_visible:
            keys.append("instagram")
        if user_profile.facebook_is_visible:
            keys.append("facebook")
        if user_profile.linkedin_is_visible:
            keys.append("linkedin")
        return (
            {
                key: str(getattr(user_profile, key)) if getattr(user_profile, key) else None
                for key in keys
            }
            if user_profile
            else None
        )

    def _get_user_profile_dict_ext(self, user_profile_ext):
        return (
            {
                key: str(getattr(user_profile_ext, key)) if getattr(user_profile_ext, key) else None
                for key in [
                    "profession",
                    "service",
                ]
            }
            if user_profile_ext
            else None
        )

    def _get_combined_data(self, user_info, user_profile, user_profile_dict, user_profile_dict_ext):
        user_data = {
            "full_name": user_info.full_name,
            "username": user_info.username,
        }
        if user_profile.email_is_visible:
            user_data["email"] = user_info.email
        return {
            "user": user_data,
            "user_profile": user_profile_dict,
            "user_profile_extended": user_profile_dict_ext,
            "portfolio": [
                {
                    "file_url": str(file.file.url) if file else None,
                }
                for file in user_info.user_files
            ],
        }

    def get(self, request, user_id, *args, **kwargs):
        user_info = self._get_user_info_or_404(user_id)

        user_profile = user_info.userprofile if hasattr(user_info, "userprofile") else None
        user_profile_dict = self._get_user_profile_dict(user_profile)

        user_profile_ext = user_info.userprofileextended if hasattr(user_info, "userprofileextended") else None
        user_profile_dict_ext = self._get_user_profile_dict_ext(user_profile_ext)

        combined_data = self._get_combined_data(user_info, user_profile, user_profile_dict, user_profile_dict_ext)

        return Response(combined_data, status=status.HTTP_200_OK)
