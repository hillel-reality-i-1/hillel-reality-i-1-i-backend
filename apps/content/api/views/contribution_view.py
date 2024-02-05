from rest_framework.generics import ListAPIView

from apps.content.api.serializers.contribution_serializer import ContributionSerializer
from apps.content.models import Comment


class ContributionListView(ListAPIView):
    serializer_class = ContributionSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post_id, is_contribution=True).order_by("-creation_date")
        return queryset
