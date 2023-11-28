# from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# from rest_framework.views import APIView
from apps.users.models import UserProfile
from apps.users.permissions import IsAdminOrProfileOwner

# from rest_framework.response import Response
from apps.users.serializers.user_profile_serializer import UserProfileSerializer


class UserProfileListView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProfileOwner]
