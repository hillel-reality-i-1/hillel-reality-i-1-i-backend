from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.conf import settings

import vonage


@permission_classes([IsAuthenticated])
class SendVonageVerificationCode(APIView):
    def post(self, request):
        user_profile = request.user.userprofile

        if user_profile.phone_verified:
            return Response({"status": "already verified"}, status=status.HTTP_200_OK)

        client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
        verify = vonage.Verify(client)

        phone_number = user_profile.phone_number
        response = verify.start_verification(number=str(phone_number), brand="U-Help")

        if response["status"] == "0":
            user_profile.phone_verified_request_id = response["request_id"]
            user_profile.save()
            return Response(
                {"detail": "Started phone_number %s verification" % phone_number},
            )
        else:
            return Response({"Error": "Failed to send verified code"}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class CheckVonageVerificationCode(APIView):
    def post(self, request):
        user_profile = request.user.userprofile
        verification_code = request.data.get("verification_code")

        if user_profile.phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
        verify = vonage.Verify(client)

        response = verify.check(user_profile.phone_verified_request_id, code=verification_code)

        if response["status"] == "0":
            user_profile.phone_verified = True
            user_profile.save()
            return Response({"status": "Verification successful"})
        else:
            return Response({"status": "Error: %s" % response["error_text"]})
