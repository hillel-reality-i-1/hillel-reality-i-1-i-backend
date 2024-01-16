from rest_framework import serializers
from apps.files.api.serializers.porfolio_serializer import PortfolioSerializer
from apps.files.models import File
from apps.users.models import UserProfileExtended, UserProfile


class UserProfileExtendedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = UserProfileExtended
        fields = (
            "id",
            "user",
            "profession",
            "service",
            "portfolio",
        )

    def get_user(self, obj):
        return obj.user.pk

    def validate_profession(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("You can add no more than 5 professions")
        return value

    def validate_service(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("You can add no more than 5 services")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["profession"] = [profession.name for profession in instance.profession.all()]
        data["service"] = [service.name for service in instance.service.all()]
        portfolio = File.objects.filter(author=instance.user)
        data["portfolio"] = PortfolioSerializer(portfolio, many=True).data
        return data

    def create(self, validated_data):
        user = validated_data.get("user")
        if UserProfile.objects.filter(user=user).exists():
            if not UserProfileExtended.objects.filter(user=user).exists():
                professions = validated_data.pop("profession", [])
                services = validated_data.pop("service", [])
                expert_user_profile = UserProfileExtended.objects.create(**validated_data)
                expert_user_profile.profession.set(professions)
                expert_user_profile.service.set(services)
            else:
                raise serializers.ValidationError("This user already has an expert profile")
        else:
            raise serializers.ValidationError(
                "In order to create an expert profile, you first need to create a user profile."
            )

        return expert_user_profile
