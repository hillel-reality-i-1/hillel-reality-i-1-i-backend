from datetime import datetime
from django.db import transaction
from allauth.account.models import EmailAddress
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import NotFound, ValidationError
from apps.users.serializers.change_email_serializer import ChangeEmailSerializer
from django.contrib.auth.hashers import check_password
from core.settings import env, ALLOWED_HOSTS, DEBUG


PORT = "8000"

if DEBUG:
    HOST = f"http://{ALLOWED_HOSTS[1]}:{PORT}"
else:
    HOST = ALLOWED_HOSTS[0]

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")


class ChangeEmailRequestView(APIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @swagger_auto_schema(request_body=ChangeEmailSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data["new_email"]
        password = serializer.validated_data["password"]

        user = request.user

        if not check_password(password, user.password):
            raise ValidationError("Wrong password.")

        # Создание и отправка письма с токеном
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        start_time = urlsafe_base64_encode(force_bytes(datetime.now()))

        email_subject = "Change email"
        email_message = (
            f"To change your email, please use this link: "
            f"{HOST}/api/v1/change-email/confirm/{uid}/{token}/?new_email={new_email}&start_time={start_time}"
        )
        send_mail(email_subject, email_message, EMAIL_HOST_USER, [new_email])

        return Response(
            {"detail": "An email with instructions has been sent to a new email address."}, status=status.HTTP_200_OK
        )


class ChangeEmailConfirmView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        new_email = request.query_params.get("new_email")
        start_time = request.query_params.get("start_time")
        start_time = urlsafe_base64_decode(start_time).decode()
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        diff = current_time - start_time

        if (diff.total_seconds() / 60) > 60:
            return Response(
                {"detail": "Sorry. The time allotted for using the link has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise NotFound("User is not found.")

        if default_token_generator.check_token(user, token):
            with transaction.atomic():
                user.email = new_email
                user.save()

                email_address = EmailAddress.objects.get(user=user)
                email_address.email = new_email
                email_address.save()
            return Response({"detail": "Email successfully changed."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Wrong token."}, status=status.HTTP_400_BAD_REQUEST)
