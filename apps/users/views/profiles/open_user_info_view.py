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

    def get(self, request, user_id, *args, **kwargs):
        user_info = get_object_or_404(
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

        user_profile = user_info.userprofile if hasattr(user_info, "userprofile") else None
        user_profile_dict = (
            {
                key: str(getattr(user_profile, key)) if getattr(user_profile, key) else None
                for key in [
                    "phone_number",
                    "about_my_self",
                    "country",
                    "city",
                    "telegram",
                    "instagram",
                    "facebook",
                    "linkedin",
                    "profile_picture",
                ]
            }
            if user_profile
            else None
        )

        user_profile_ext = user_info.userprofileextended if hasattr(user_info, "userprofileextended") else None
        user_profile_dict_ext = (
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

        combined_data = {
            "user": {
                "email": user_info.email,
                "full_name": user_info.full_name,
                "username": user_info.username,
            },
            "user_profile": user_profile_dict,
            "user_profile_extended": user_profile_dict_ext,
            "portfolio": [
                {
                    "file_url": str(file.file.url) if file else None,
                }
                for file in user_info.user_files
            ],
        }

        return Response(combined_data, status=status.HTTP_200_OK)
