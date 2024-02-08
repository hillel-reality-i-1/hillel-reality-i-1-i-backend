from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from apps.users.models import UserProfile, UserProfileExtended
from apps.users.permissions import IsAdminOrProfileOwner
from apps.users.serializers.user_profile_serializer import UserProfileSerializer


class UserProfileListView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProfileOwner]

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            user_profile_extended = UserProfileExtended.objects.get(user=instance.user)
            user_profile_extended.delete()
        except UserProfileExtended.DoesNotExist:
            pass
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
