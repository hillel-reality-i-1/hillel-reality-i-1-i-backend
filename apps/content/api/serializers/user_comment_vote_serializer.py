from rest_framework import serializers

from apps.content.models import UserCommentVote


class UserCommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommentVote
        fields = ("id", "user", "comment", "helpful")
