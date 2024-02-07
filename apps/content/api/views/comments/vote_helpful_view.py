from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from apps.content.models import Comment
from apps.content.models.comment import UserCommentVote
from apps.users.permissions import IsVerifiedUser


class VoteHelpfulView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def handle_vote(self, request, comment_id, helpful):
        comment = Comment.objects.get(pk=comment_id)

        if not comment.is_parent:
            raise serializers.ValidationError("Вы не можете голосовать за вложенные комментарии.")

        user = request.user

        existing_vote = UserCommentVote.objects.filter(user=user, comment=comment).first()

        if existing_vote:
            if existing_vote.helpful == helpful:
                existing_vote.delete()
                if helpful:
                    comment.vote_helpful_state = False
                else:
                    comment.vote_not_helpful_state = False
            else:
                existing_vote.helpful = helpful
                existing_vote.save()
                comment.vote_helpful_state = helpful
                comment.vote_not_helpful_state = not helpful
        else:
            UserCommentVote.objects.create(user=user, comment=comment, helpful=helpful)
            comment.vote_helpful_state = helpful
            comment.vote_not_helpful_state = not helpful

        comment.update_vote_counts()
        comment.save()

        return Response(status=status.HTTP_200_OK)

    def post(self, request, comment_id):
        return self.handle_vote(request, comment_id, helpful=True)


class VoteNotHelpfulView(VoteHelpfulView):
    def post(self, request, comment_id):
        return self.handle_vote(request, comment_id, helpful=False)
