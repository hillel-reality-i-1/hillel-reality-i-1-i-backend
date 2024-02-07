from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.content.utils.aws_utils import moderation_image_with_aws, moderate_img
from apps.files.api.serializers import ImageSerializer
from apps.files.models import Image
from apps.users.permissions import IsAdminOrImageOwner


class ImageListView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrImageOwner]

    def update(self, request, *args, **kwargs):
        print("v update")
        current_image = Image.objects.filter(author=self.request.user).first()
        prev_image = current_image.image if current_image else None
        if current_image:
            prev_image_path = current_image.image.url.split("/")
            prev_image_path = "/".join(prev_image_path[1:])
        else:
            prev_image_path = None

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        path = serializer.data.get("image").split("/")
        path = "/".join(path[3:])
        response = moderation_image_with_aws(path)
        moderate_img(Image, response, path, serializer, prev_image, prev_image_path, "image")

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        print("perform_update")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
