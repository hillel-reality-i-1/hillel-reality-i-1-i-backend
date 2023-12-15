from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.users.models import UserProfileExtended
from apps.users.permissions import IsAdminOrProfileExtendedOwner
from apps.users.serializers.user_profile_extended_serializer import UserProfileExtendedSerializer


class UserProfileExtendedListView(viewsets.ModelViewSet):
    queryset = UserProfileExtended.objects.all()
    serializer_class = UserProfileExtendedSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProfileExtendedOwner]
