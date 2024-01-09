from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.users.models import UserProfileExtended
from apps.users.permissions import IsAdminOrExpertUserProfileOwner
from apps.users.serializers.user_profile_extended_serializer import UserProfileExtendedSerializer


class ExpertUserProfileByUserIdView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrExpertUserProfileOwner,
    ]

    def get(self, request, user_id, *args, **kwargs):
        expert_user_profile = get_object_or_404(UserProfileExtended, user__id=user_id)
        serializer = UserProfileExtendedSerializer(expert_user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
