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

frontend_url = "http://127.0.0.1:8000"


class ChangeEmailRequestView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ChangeEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data["new_email"]
        password = serializer.validated_data["password"]

        user = request.user

        if not check_password(password, user.password):
            raise ValidationError("Wrong password.")

        # Создание и отправка письма с токеном
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        email_subject = "Change email"
        email_message = (
            f"To change your email, please use this link: "
            f"{frontend_url}/api/v1/change-email/confirm/{uid}/{token}/?new_email={new_email}"
        )
        send_mail(email_subject, email_message, "from@example.com", [new_email])

        return Response(
            {"detail": "An email with instructions has been sent to a new email address."}, status=status.HTTP_200_OK
        )


class ChangeEmailConfirmView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        new_email = request.query_params.get("new_email")
        print(new_email)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise NotFound("User is not found.")

        if default_token_generator.check_token(user, token):
            user.email = new_email
            user.save()
            return Response({"detail": "Email successfully changed."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Wrong token."}, status=status.HTTP_400_BAD_REQUEST)
