from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.content.api.serializers import CommentSerializer
from apps.content.models import Comment
from apps.content.permissions import IsAuthorOrReadOnly


class CommentDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.destroy(instance)
        return Response({"message": "Коментар успішно видалено"}, status=status.HTTP_204_NO_CONTENT)
