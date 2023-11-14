from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

# from rest_framework.views import APIView
from apps.users.models import UserProfileExtended
from apps.users.serializers.user_profile_extended_serializer import UserProfileExtendedSerializer

# from rest_framework.response import Response


class UserProfileExtendedListView(viewsets.ModelViewSet):
    queryset = UserProfileExtended.objects.all()
    serializer_class = UserProfileExtendedSerializer
    permission_classes = [IsAdminUser]
