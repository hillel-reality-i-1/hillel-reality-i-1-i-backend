from django.db import transaction
from allauth.account.models import EmailAddress
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import NotFound, ValidationError

from apps.users.adapters import CustomAdapter
from apps.users.serializers.change_email_serializer import ChangeEmailSerializer
from django.contrib.auth.hashers import check_password

from apps.users.token_generators import EmailChangeTokenGenerator


token_generator = EmailChangeTokenGenerator()


class ChangeEmailRequestView(APIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    adapter_class = CustomAdapter

    def get_adapter(self):
        return self.adapter_class()

    @swagger_auto_schema(request_body=ChangeEmailSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data["new_email"]
        password = serializer.validated_data["password"]

        user = request.user

        if not check_password(password, user.password):
            raise ValidationError("Wrong password.")

        if get_user_model().objects.filter(email=new_email).exists():
            raise ValidationError("User with such email has already been created.")

        # Создание и отправка письма с токеном
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        self.get_adapter().send_email_change_mail(uid, token, new_email)

        return Response(
            data={"detail": "An email with instructions has been sent to a new email address."},
            status=status.HTTP_200_OK,
        )


class ChangeEmailConfirmView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        new_email = request.query_params.get("new_email")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise NotFound("User is not found.")

        if token_generator.check_token(user, token):
            with transaction.atomic():
                user.email = new_email
                user.save()

                email_address = EmailAddress.objects.get(user=user)
                email_address.email = new_email
                email_address.save()
            return Response({"detail": "Email successfully changed."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Wrong token."}, status=status.HTTP_400_BAD_REQUEST)
