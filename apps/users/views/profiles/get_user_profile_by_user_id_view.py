from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.users.models import UserProfile
from apps.users.permissions import IsAdminOrUserProfileOwner
from apps.users.serializers.user_profile_serializer import UserProfileSerializer


class UserProfileByUserIdView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrUserProfileOwner,
    ]

    def get(self, request, user_id, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
