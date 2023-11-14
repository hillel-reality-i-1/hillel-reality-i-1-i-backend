from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

# from rest_framework.views import APIView
from apps.users.models import UserProfile

# from rest_framework.response import Response
from apps.users.serializers.user_profile_serializer import UserProfileSerializer


class UserProfileListView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]


# class UserProfileListView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         profiles = UserProfile.objects.all()
#         serializer = UserProfileSerializer(profiles, many=True)
#         return Response(serializer.data)
