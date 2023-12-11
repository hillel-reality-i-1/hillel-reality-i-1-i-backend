# from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from rest_framework.views import APIView
from apps.users.models import UserProfile
from apps.users.permissions import IsAdminOrProfileOwner

# from rest_framework.response import Response
from apps.users.serializers.user_profile_serializer import UserProfileSerializer


class UserProfileListView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProfileOwner]

    def get_object(self):
        return self.request.user.userprofile

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
