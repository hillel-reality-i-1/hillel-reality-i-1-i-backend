from rest_framework.generics import ListAPIView

from apps.content.api.serializers.contribution_serializer import ContributionSerializer
from apps.content.models import Comment
from apps.users.views.last_activity.last_activity_pagination import LastFiveActivityPagination


class ContributionListView(ListAPIView):
    serializer_class = ContributionSerializer
    pagination_class = LastFiveActivityPagination

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        queryset = Comment.objects.filter(post_id=post_id, is_contribution=True).order_by("-creation_date")
        return queryset
