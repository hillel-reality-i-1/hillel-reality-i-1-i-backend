from rest_framework import serializers
from apps.expert.models import Profession, Service
from apps.expert.serializers import ProfessionSerializer, ServiceSerializer
from apps.files.api.serializers.porfolio_serializer import PortfolioSerializer
from apps.files.models import File
from apps.users.models import UserProfileExtended


class UserProfileExtendedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    portfolio = PortfolioSerializer(read_only=True)
    profession = ProfessionSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    profession_id = serializers.PrimaryKeyRelatedField(
        queryset=Profession.objects.all(), source="profession", write_only=True, required=False, allow_null=True
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = UserProfileExtended
        fields = (
            "id",
            "user",
            "profession",
            "service",
            "profession_id",
            "service_id",
            "portfolio",
        )

    def get_user(self, obj):
        return obj.user.pk

    def to_representation(self, instance):
        data = super().to_representation(instance)
        portfolio = File.objects.filter(author=instance.user)
        data["portfolio"] = PortfolioSerializer(portfolio, many=True).data
        return data
