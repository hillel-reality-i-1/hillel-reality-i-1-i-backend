from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.content.api.serializers import ContributionSerializer
from apps.content.models import Contribution


class ContributionListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = ContributionSerializer

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return Contribution.objects.filter(post_id=post_id)
