from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.content.models import Comment
from apps.content.models.comment import UserCommentVote
from apps.users.permissions import IsVerifiedUser


class VoteHelpfulView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def handle_vote(self, request, comment_id, helpful):
        comment = Comment.objects.get(pk=comment_id)

        if not comment.is_parent:
            return Response({"detail": "You cannot vote on nested comments."}, status=status.HTTP_403_FORBIDDEN)

        user = request.user

        existing_vote = UserCommentVote.objects.filter(user=user, comment=comment).first()

        if existing_vote:
            if existing_vote.helpful == helpful:
                existing_vote.delete()
            else:
                existing_vote.helpful = helpful
                existing_vote.save()
        else:
            UserCommentVote.objects.create(user=user, comment=comment, helpful=helpful)

        comment.update_vote_counts()

        return Response(status=status.HTTP_200_OK)

    def post(self, request, comment_id):
        return self.handle_vote(request, comment_id, helpful=True)


class VoteNotHelpfulView(VoteHelpfulView):
    def post(self, request, comment_id):
        return self.handle_vote(request, comment_id, helpful=False)
