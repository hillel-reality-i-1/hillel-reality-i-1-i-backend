from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from apps.users.models import User
from apps.content.api.serializers import PostSerializer
from apps.users.views.last_activity.last_activity_pagination import LastFiveActivityPagination


class LastPostsByAuthor(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LastFiveActivityPagination

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)

        return user.post_set.order_by("-creation_date")
