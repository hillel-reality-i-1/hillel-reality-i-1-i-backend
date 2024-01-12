from rest_framework import serializers
from apps.expert.models import Profession, Service
from apps.expert.serializers import ProfessionSerializer, ServiceSerializer
from apps.files.api.serializers.porfolio_serializer import PortfolioSerializer
from apps.files.models import File
from apps.users.models import UserProfileExtended, UserProfile


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

    def create(self, validated_data):
        user = validated_data.get("user")
        if UserProfile.objects.filter(user=user).exists():
            if not UserProfileExtended.objects.filter(user=user).exists():
                expert_user_profile = UserProfileExtended.objects.create(**validated_data)
            else:
                raise serializers.ValidationError("This user already has an expert profile")
        else:
            raise serializers.ValidationError(
                "In order to create an expert profile, " "you first need to create a user profile."
            )

        return expert_user_profile
