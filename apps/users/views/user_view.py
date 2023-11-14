# from rest_framework import status
from rest_framework.permissions import IsAdminUser

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from apps.users.models import User
from apps.users.serializers.user_serializer import UserSerializer
from rest_framework import viewsets


class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


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
