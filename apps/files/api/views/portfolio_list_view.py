from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.content.utils.aws_utils import moderation_image_with_aws, moderate_img
from apps.files.api.serializers.porfolio_serializer import PortfolioSerializer
from apps.files.models import File
from apps.users.permissions import IsAdminOrPortfolioOwner


class PortfolioListView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = File.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPortfolioOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        print("v update")
        current_image = self.get_object()

        prev_image = current_image.file
        prev_image_path = current_image.file.url.split("/")
        prev_image_path = "/".join(prev_image_path[1:])

        serializer = self.get_serializer(current_image, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        path = serializer.data.get("file").split("/")
        path = "/".join(path[3:])
        response = moderation_image_with_aws(path)
        moderate_img(File, response, path, serializer, prev_image, prev_image_path, "file")

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        print("perform_update")
        serializer.save()
