from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.files.api.serializers import ImageSerializer
from apps.files.models import Image
from apps.users.permissions import IsAdminOrAvatarOwner


class ImageByUserIdView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrAvatarOwner,
    ]

    def get(self, request, user_id, *args, **kwargs):
        image = get_object_or_404(Image, author=user_id)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
