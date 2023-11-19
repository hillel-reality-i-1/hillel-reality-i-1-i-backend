from django.utils import timezone
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegistrationSerializer(RegisterSerializer):
    declared_fields = RegisterSerializer.__dict__["_declared_fields"]

    declared_fields.pop("password1")
    declared_fields.pop("password2")
    declared_fields.pop("username")
    declared_fields["password"] = serializers.CharField(write_only=True)
    declared_fields["first_name"] = serializers.CharField(write_only=True)
    declared_fields["last_name"] = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password": self.validated_data.get("password", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def save(self, request):
        user = super().save(request)

        cleaned_data = self.get_cleaned_data()
        user.first_name = cleaned_data["first_name"]
        user.last_name = cleaned_data["last_name"]
        password = cleaned_data["password"]
        user.email = cleaned_data["email"]

        user.set_password(password)
        user.date_joined = timezone.now()

        user.save()
        return user
