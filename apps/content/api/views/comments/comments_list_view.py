from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.content.api.serializers import CommentSerializer
from apps.content.models import Comment


class CommentsListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return Comment.objects.filter(post_id=post_id, parent=None)
