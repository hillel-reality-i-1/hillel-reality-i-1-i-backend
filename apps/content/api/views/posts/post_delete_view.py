from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.content.api.serializers import PostSerializer
from apps.content.models import Post
from apps.content.permissions import IsAuthorOrReadOnly


class PostDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.destroy(instance)
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response({"message": "Допис успішно видалено"}, status=status.HTTP_204_NO_CONTENT)
