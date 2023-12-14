from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from apps.files.api.serializers import ImageSerializer
from apps.files.models import Image
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UploadImageView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
