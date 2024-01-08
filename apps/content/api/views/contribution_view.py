from rest_framework.generics import ListAPIView

from apps.content.api.serializers.contribution_serializer import ContributionSerializer
from apps.content.models import Comment


class ContributionListView(ListAPIView):
    serializer_class = ContributionSerializer
    queryset = Comment.objects.filter(is_contribution=True).order_by("-creation_date")
