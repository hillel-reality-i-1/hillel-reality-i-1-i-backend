from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from apps.users.models import User


class CustomRegistrationSerializer(RegisterSerializer):
    declared_fields = RegisterSerializer.__dict__["_declared_fields"]
    declared_fields.pop("username")

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        if not User.objects.filter(email=cleaned_data["email"]).exists():
            user = super().save(request)
        else:
            raise serializers.ValidationError("This email is already in use. Please, use another or sign in")

        user.first_name = "Anonim"

        user.save()
        return user
