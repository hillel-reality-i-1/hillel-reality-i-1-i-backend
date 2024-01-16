from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import UserProfileExtended
from apps.users.serializers.user_profile_extended_serializer import UserProfileExtendedSerializer


class RegisterProfileExtView(generics.CreateAPIView):
    serializer_class = UserProfileExtendedSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfileExtended.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
