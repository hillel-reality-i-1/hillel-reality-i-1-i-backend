from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.content.models import Comment
from apps.content.permissions import IsAuthorOrReadOnly
from apps.content.api.serializers import CommentSerializer


class CommentModifiedDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        comment = self.get_object()

        if comment.usercommentvote_set.exists():
            raise serializers.ValidationError("Ви не можете редагувати запис із реакціями")

        if comment.replies.exists():
            raise serializers.ValidationError("Ви не можете редагувати запис із коментарями")

        serializer.save()
