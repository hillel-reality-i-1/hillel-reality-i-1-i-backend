from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers.user_profile_serializer import UserProfileSerializer


class RegisterProfileView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
