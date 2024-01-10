from rest_framework import status
from rest_framework.generics import DestroyAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from ..permissions import IsVerifiedUser
from ..serializers.user_serializer import UserSerializer


class UserDeleteView(DestroyAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsVerifiedUser]

    def get_object(self):
        obj = self.queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={"details": "Your account has been successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
