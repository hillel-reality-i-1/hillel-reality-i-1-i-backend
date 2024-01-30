from django.conf import settings
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client


def send_twilio_verification_code(user_profile):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    verification = client.verify.v2.services(settings.TWILIO_VERIFY_SID).verifications.create(
        to=str(user_profile.phone_number), channel="sms"
    )

    user_profile.twilio_verification_sid = verification.sid
    user_profile.save()

    return verification.status


@permission_classes([IsAuthenticated])
class SendTwilioVerificationCode(APIView):
    def post(self, request):
        user_profile = request.user.userprofile

        if user_profile.phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        send_twilio_verification_code(user_profile)

        return Response(
            {"status": "Started phone_number %s verification" % user_profile.phone_number}, status=status.HTTP_200_OK
        )
