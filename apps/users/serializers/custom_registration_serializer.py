from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from apps.users.models import User


class CustomRegistrationSerializer(RegisterSerializer):
    declared_fields = RegisterSerializer.__dict__["_declared_fields"]
    declared_fields.pop("username")

    def validate(self, data):
        self.validate_passwords(data)
        return super().validate(data)

    def validate_email(self, value):
        if EmailAddress.objects.filter(email=value, verified=True).exists():
            raise serializers.ValidationError("This email is already in use. Please, use another or sign in")

        return value

    @staticmethod
    def validate_passwords(data):
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("Passwords do not match")

    def save(self, request):
        user = super().save(request)
        # user.full_name = "Anonim User"
        # user.first_name = "Anonim"
        # user.last_name = "User"
        # user.save()
        return user
