from allauth.account.adapter import get_adapter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsVerifiedUser
from apps.users.token_generators import DeleteAllContentTokenGenerator


class DeleteAllContentView(APIView):
    permission_classes = [IsVerifiedUser]

    def post(self, request, *args, **kwargs):

        key = DeleteAllContentTokenGenerator().make_token(request.user)
        get_adapter().send_delete_all_content_confirmation_mail(request.user, key)

        return Response({"detail": "Confirmation email sent successfully."}, status=status.HTTP_200_OK)
