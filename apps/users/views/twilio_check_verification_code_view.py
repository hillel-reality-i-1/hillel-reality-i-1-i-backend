from django.conf import settings
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client


def check_twilio_verification_code(user_profile, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SID).verification_checks.create(
        to=str(user_profile.phone_number), code=verification_code
    )

    if verification_check.status == "approved":
        user_profile.phone_verified = True
        user_profile.save()
        return "approved"
    else:
        return "invalid"


@permission_classes([IsAuthenticated])
class CheckTwilioVerificationCode(APIView):
    def post(self, request):
        user_profile = request.user.userprofile
        verification_code = request.data.get("verification_code")

        if user_profile.phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        verification_status = check_twilio_verification_code(user_profile, verification_code)

        if verification_status == "approved":
            return Response({"status": "Verification successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "invalid"}, status=status.HTTP_400_BAD_REQUEST)
