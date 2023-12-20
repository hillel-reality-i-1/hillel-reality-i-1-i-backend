# from rest_framework import status
# from rest_framework.permissions import IsAdminUser

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.users.models import User
from apps.users.permissions import IsAdminOrSelf
from apps.users.serializers.user_serializer import UserSerializer
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response


class UserListView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if "username" in request.data:
            if instance.username_changed:
                return Response({"detail": "You can not change the username"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.username_changed = True

        self.perform_update(serializer)

        return Response(serializer.data)


# class UserListView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserDetailView(RetrieveUpdateAPIView, DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]
