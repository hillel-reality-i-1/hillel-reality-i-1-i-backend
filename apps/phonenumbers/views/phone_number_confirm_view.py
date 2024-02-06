from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.phonenumbers.models import PhoneNumber
from apps.phonenumbers.serializers import VerificationCodeSerializer


def check_alpha_sms_verification_code(user_profile, verification_code):
    hash_verification_code = PhoneNumber.hash_function(verification_code)
    phone_number = PhoneNumber.objects.filter(
        number=str(user_profile.phone_number),
        verification_code_hashed=hash_verification_code
    ).first()

    if phone_number:
        if timezone.now() > phone_number.verification_code_timestamp + timedelta(seconds=settings.SMS_VERIFY_TIMEOUT):
            phone_number.delete()
            return "expired"
        user_profile.phone_verified = True
        user_profile.save()
        phone_number.delete()
        return "approved"
    else:
        return "invalid"


class PhoneNumberConfirmView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = VerificationCodeSerializer

    def post(self, request):
        user_profile = request.user.userprofile
        verification_code = request.data.get("verification_code")

        if user_profile.phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        verification_status = check_alpha_sms_verification_code(user_profile, verification_code)

        if verification_status == "expired":
            return Response({"status": "Verification code is expired"}, status=status.HTTP_400_BAD_REQUEST)

        if verification_status == "approved":
            return Response({"status": "Verification successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "invalid"}, status=status.HTTP_400_BAD_REQUEST)
