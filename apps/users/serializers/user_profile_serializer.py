from rest_framework import serializers
from apps.files.api.serializers import ImageSerializer
from apps.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)
    profile_picture = ImageSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"

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
        instance.about_my_self = validated_data.get("about_my_self", instance.about_my_self)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)

        instance.save()
        return instance

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
