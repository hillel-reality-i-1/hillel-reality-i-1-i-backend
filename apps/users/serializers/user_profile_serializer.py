from cities_light.models import Country, City
from rest_framework import serializers
from apps.files.api.serializers import ImageSerializer
from apps.location.serializers.city_serializer import CitySerializer
from apps.location.serializers.country_serializer import CountrySerializer
from apps.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)
    profile_picture = ImageSerializer(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source="country", write_only=True, required=False, allow_null=True
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = (
            "twilio_phone_verified",
            "twilio_verification_sid",
            "phone_verified",
            "phone_verified_request_id",
        )

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_user(self, obj):
        return obj.user.pk

    def create(self, validated_data):
        user = validated_data.get("user")
        if not UserProfile.objects.filter(user=user).exists():
            user_profile = UserProfile.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("This user already has a profile")

        return user_profile

    def update(self, instance, validated_data):
        new_phone_number = validated_data.get("phone_number")

        if new_phone_number:
            instance.phone_number = new_phone_number
            instance.phone_verified = False
            instance.twilio_verification_sid = None
            instance.phone_verified_request_id = None

        instance.about_my_self = validated_data.get("about_my_self", instance.about_my_self)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)

        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     instance.about_my_self = validated_data.get("about_my_self", instance.about_my_self)
    #     instance.country = validated_data.get("country", instance.country)
    #     instance.city = validated_data.get("city", instance.city)
    #     instance.phone_number = validated_data.get("phone_number", instance.phone_number)
    #
    #     instance.save()
    #     return instance
