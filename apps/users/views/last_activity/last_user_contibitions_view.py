from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.api.serializers import CommentSerializer
from apps.users.models import UserProfile


class LastUserContributions(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        return user_profile.last_contributions.order_by("-updated_date")
