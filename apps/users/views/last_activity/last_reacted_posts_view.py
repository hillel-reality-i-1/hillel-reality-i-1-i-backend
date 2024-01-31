from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from apps.users.models import UserProfile
from apps.content.api.serializers import PostSerializer
from apps.users.views.last_activity.last_activity_pagination import LastFiveActivityPagination


class LastReactedPostsView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LastFiveActivityPagination

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user_profile = get_object_or_404(UserProfile, user_id=user_id)

        return user_profile.last_reacted_posts.order_by("-reactions__creation_date")
