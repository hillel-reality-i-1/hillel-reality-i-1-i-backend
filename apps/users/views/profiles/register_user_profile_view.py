from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.users.models import UserProfile
from apps.users.serializers.user_profile_serializer import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterProfileView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
