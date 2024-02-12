from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from apps.content.models import Comment
from apps.content.permissions import IsAuthorOrReadOnly
from apps.content.api.serializers import CommentSerializer


class CommentModifiedView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthorOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        comment = self.get_object()

        if comment.usercommentvote_set.exists():
            raise serializers.ValidationError("Ви не можете редагувати запис із реакціями")

        if comment.replies.exists():
            raise serializers.ValidationError("Ви не можете редагувати запис із коментарями")

        serializer.save()
