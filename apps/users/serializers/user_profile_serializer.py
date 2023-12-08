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
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
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

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

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

    # def update(self, instance, validated_data):
    #     instance.about_my_self = validated_data.get("about_my_self", instance.about_my_self)
    #     instance.country = validated_data.get("country", instance.country)
    #     instance.city = validated_data.get("city", instance.city)
    #     instance.phone_number = validated_data.get("phone_number", instance.phone_number)
    #
    #     instance.save()
    #     return instance

    # # ##### виталик!!!!!!!
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #
    #     country_result = get_places(settings.GOOGLE_API_KEY, data['country'])
    #     if country_result:
    #         country_info = next((place for place in country_result if 'country' in place.get('types', [])), None)
    #         if country_info:
    #             data['country'] = {
    #                 'name': country_info.get('description', ''),
    #             }
    #
    #             city_result = get_places(settings.GOOGLE_API_KEY, f"{data['city']} {data['country']['name']}")
    #             city_info = next((place for place in city_result if 'locality' in place.get('types', [])), None)
    #             if city_info:
    #                 data['city'] = {
    #                     'name': city_info.get('description', ''),
    #                 }
    #
    #     return data
