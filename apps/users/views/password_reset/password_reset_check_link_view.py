from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import PasswordResetCheckLinkSerializer


class PasswordResetCheckAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetCheckLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data={'details': True}, status=status.HTTP_200_OK)
