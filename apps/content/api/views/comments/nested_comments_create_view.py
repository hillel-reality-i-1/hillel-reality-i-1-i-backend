from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.api.serializers import CommentSerializer
from apps.content.models import Comment
from apps.users.permissions import IsVerifiedUser


class NestedCommentsCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def perform_create(self, serializer):
        parent_id = self.kwargs["pk"]
        parent_comment = get_object_or_404(Comment, pk=parent_id)

        if parent_comment.parent:
            """
            комменты привязываются к самому верхнему комментарию в ветке
            """
            while parent_comment.parent:
                parent_comment = parent_comment.parent

        user = self.request.user

        serializer.save(author=user, post=parent_comment.post, parent=parent_comment, is_parent=False)
