from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import Contribution
from apps.content.models.contribution import ContributionVote
from apps.users.permissions import IsVerifiedUser


class VoteContributionView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def post(self, request, pk):
        contribution = Contribution.objects.get(pk=pk)

        user = request.user

        existing_vote = ContributionVote.objects.filter(user=user, contribution=contribution).first()

        if existing_vote:
            existing_vote.delete()
        else:
            ContributionVote.objects.create(user=user, contribution=contribution, helpful=True)

        contribution.update_counts()

        return Response({"detail": "Vote recorded successfully."}, status=status.HTTP_200_OK)
