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

        if user_profile.twilio_phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        account_sid = "ACc23fd207ba2533bb2eb9ea20698df50b"
        auth_token = "b2bfb38818516ecaace7c21e6783f644"
        verify_sid = "VAbd62216f012ec5791a63e3c85a587e44"
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

        if user_profile.twilio_phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        account_sid = "ACc23fd207ba2533bb2eb9ea20698df50b"
        auth_token = "b2bfb38818516ecaace7c21e6783f644"
        verify_sid = "VAbd62216f012ec5791a63e3c85a587e44"
        client = Client(account_sid, auth_token)

        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
            to=str(user_profile.phone_number), code=verification_code
        )

        if verification_check.status == "approved":
            user_profile.twilio_phone_verified = True
            user_profile.save()
            return Response({"status": "approved"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "invalid"}, status=status.HTTP_400_BAD_REQUEST)


# import vonage
#
# client = vonage.Client(key="785c35b9", secret="Y3AsLmpss9lf4VXO")
# verify = vonage.Verify(client)
#
# response = verify.start_verification(number="380631221640", brand="U-Help")
#
# if response["status"] == "0":
#     print("Started verification request_id is %s" % (response["request_id"]))
# else:
#     print("Error: %s" % response["error_text"])
#
# my_code = input("Code: ")
# response = verify.check(response["request_id"], code=my_code)
#
# if response["status"] == "0":
#     print("Verification successful, event_id is %s" % (response["event_id"]))
# else:
#     print("Error: %s" % response["error_text"])
