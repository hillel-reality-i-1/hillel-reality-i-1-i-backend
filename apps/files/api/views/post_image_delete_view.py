from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.files.api.serializers.post_image_serializer import PostImageSerializer
from apps.files.models.post_image import PostImage


class PostImageDeleteView(RetrieveDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.destroy(instance)
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response({"message": "Зображення успішно видалено"}, status=status.HTTP_204_NO_CONTENT)
