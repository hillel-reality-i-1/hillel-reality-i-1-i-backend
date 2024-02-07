from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.content.api.serializers.user_comment_vote_serializer import UserCommentVoteSerializer
from apps.content.models import UserCommentVote


@api_view(["GET"])
def user_comment_vote_detail(request, user_id, comment_id):
    try:
        user_comment_vote = UserCommentVote.objects.get(user_id=user_id, comment_id=comment_id)
        serializer = UserCommentVoteSerializer(user_comment_vote)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserCommentVote.DoesNotExist:
        return Response({"message": "UserCommentVote not found"}, status=status.HTTP_404_NOT_FOUND)
