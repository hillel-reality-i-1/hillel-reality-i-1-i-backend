from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.content.api.serializers import CommentSerializer
from apps.content.models import Comment
from apps.users.views.last_activity.last_activity_pagination import LastFiveActivityPagination


class CommentsListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LastFiveActivityPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        queryset = Comment.objects.filter(post_id=post_id, parent=None).order_by("-creation_date")
        return queryset
