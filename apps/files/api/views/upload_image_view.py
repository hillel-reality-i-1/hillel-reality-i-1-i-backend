from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from apps.content.utils.aws_utils import moderation_image_with_aws, moderate_img
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
        current_image = Image.objects.filter(author=self.request.user).first()
        prev_image = current_image.image if current_image else None
        if current_image:
            prev_image_path = current_image.image.url.split("/")
            prev_image_path = "/".join(prev_image_path[1:])
        else:
            prev_image_path = None

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        path = serializer.data.get("image").split("/")
        path = "/".join(path[3:])
        response = moderation_image_with_aws(path)
        moderate_img(Image, response, path, serializer, prev_image, prev_image_path, "image")

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
