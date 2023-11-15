from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers.user_profile_extended_serializer import UserProfileExtendedSerializer


class RegisterProfileExtView(generics.CreateAPIView):
    serializer_class = UserProfileExtendedSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
