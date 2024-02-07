import alphasms
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from apps.users.models import UserProfile
from ..api_classes import AlphaSMSAPI

from ..models import PhoneNumber


class PhoneNumberVerifyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_profile = request.user.userprofile

        if (
                user_profile.phone_number
                and UserProfile.objects.filter(
                    phone_number=user_profile.phone_number,
                    phone_verified=True
                ).exists()
        ):
            return Response({"status": "This number has already been verified"})

        if user_profile.phone_verified:
            return Response({"status": "already_verified"}, status=status.HTTP_200_OK)

        phone_number = PhoneNumber.objects.create()
        phone_number.number = str(user_profile.phone_number)
        verification_code = phone_number.generate_verification_code()
        phone_number.save()

        try:
            api_key = settings.ALPHA_SMS_API_KEY
            alpha_name = settings.ALPHA_SMS_ALPHA_NAME
            a = AlphaSMSAPI(api_key, alpha_name)
            a.send_sms(
                to_addr=phone_number.number,
                message=f'Код верифікації: {verification_code}'
            )
        except Exception as e:
            print("Error while sending SMS:", str(e))
            return Response(
                data={'detail': 'Error while sending SMS.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={
                "status": "Started phone_number %s verification" % phone_number.number
            },
            status=status.HTTP_200_OK
        )
