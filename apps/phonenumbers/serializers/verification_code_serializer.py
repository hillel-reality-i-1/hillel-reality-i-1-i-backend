from rest_framework import serializers


class VerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField()
