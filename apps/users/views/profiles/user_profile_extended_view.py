from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from apps.users.models import UserProfileExtended
from apps.users.permissions import IsAdminOrProfileExtendedOwner
from apps.users.serializers.user_profile_extended_serializer import UserProfileExtendedSerializer


class UserProfileExtendedListView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = UserProfileExtended.objects.all()
    serializer_class = UserProfileExtendedSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProfileExtendedOwner]
