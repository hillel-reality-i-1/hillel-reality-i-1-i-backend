from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@permission_classes([IsAuthenticated])
class SendTwilioVerificationCode(APIView):
    def post(self, request):
        user_profile = request.user.userprofile

        if user_profile.twilio_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        account_sid = "ACe52a664583f7732652f8c2069a5b480d"
        auth_token = "df5de515682c0a21e6172d027cb056ed"
        verify_sid = "VA7d3bbb583680cc5fec2d80ba58083184"
        client = Client(account_sid, auth_token)

        verification = client.verify.v2.services(verify_sid).verifications.create(
            to=str(user_profile.phone_number), channel="sms"
        )

        user_profile.twilio_verification_sid = verification.sid
        user_profile.save()

        return Response({"status": verification.status}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class CheckTwilioVerificationCode(APIView):
    def post(self, request):
        user_profile = request.user.userprofile
        verification_code = request.data.get("verification_code")

        if user_profile.twilio_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        account_sid = "ACe52a664583f7732652f8c2069a5b480d"
        auth_token = "df5de515682c0a21e6172d027cb056ed"
        verify_sid = "VA7d3bbb583680cc5fec2d80ba58083184"
        client = Client(account_sid, auth_token)

        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
            to=str(user_profile.phone_number), code=verification_code
        )

        if verification_check.status == "approved":
            user_profile.twilio_verified = True
            user_profile.save()
            return Response({"status": "verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "invalid"}, status=status.HTTP_400_BAD_REQUEST)
