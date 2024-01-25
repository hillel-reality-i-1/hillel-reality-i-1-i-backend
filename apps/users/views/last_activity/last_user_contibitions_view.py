from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.api.serializers import CommentSerializer
from apps.users.models import UserProfile


class LastUserContributions(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile_id = self.kwargs.get("profile_id")
        user_profile = get_object_or_404(UserProfile, id=profile_id)
        return user_profile.last_contributions.order_by("-creation_date")
