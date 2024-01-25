from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.content.api.serializers import CommentSerializer
from apps.users.models import UserProfile
from apps.users.views.last_activity.last_activity_pagination import LastFiveActivityPagination


class LastCommentsByAuthor(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = LastFiveActivityPagination

    def get_queryset(self):
        profile_id = self.kwargs["profile_id"]
        user_profile = get_object_or_404(UserProfile, id=profile_id)

        return user_profile.last_comments.order_by("-creation_date")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
