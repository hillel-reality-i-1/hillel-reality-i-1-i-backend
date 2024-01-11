from cities_light.models import Country, City
from rest_framework import serializers
from apps.content.api.serializers import PostSerializer, CommentSerializer, SavedPostSerializer, SavedCommentSerializer
from apps.files.api.serializers import ImageSerializer
from apps.location.serializers.city_serializer import CitySerializerNew

# from apps.location.serializers.city_serializer import CitySerializer
from apps.location.serializers.country_serializer import CountrySerializer
from apps.users.models import UserProfile
import re

# from django.utils.translation import get_language


# class CitySerializerNew(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = City
#         fields = [
#             "id",
#             "name",
#             "country",
#         ]
#
#     def get_name(self, obj):
#         language = get_language()
#         return obj.alternate_names if language == "uk" else obj.name


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)
    profile_picture = ImageSerializer(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    country = CountrySerializer(read_only=True)
    city = CitySerializerNew(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), write_only=True, required=False, allow_null=True
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), write_only=True, required=False, allow_null=True
    )

    saved_posts = SavedPostSerializer(many=True, read_only=True)
    saved_comments = SavedCommentSerializer(many=True, read_only=True)

    telegram = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)
    instagram = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)
    facebook = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=200)
    linkedin = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=200)

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = (
            "twilio_verification_sid",
            "phone_verified",
            "saved_posts",
            "saved_comments",
        )

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_user(self, obj):
        return obj.user.pk

    def get_saved_posts(self, obj):
        saved_posts = obj.saved_posts.all()
        return PostSerializer(saved_posts, many=True).data

    def get_saved_comments(self, obj):
        saved_comments = obj.saved_comments.all()
        return CommentSerializer(saved_comments, many=True).data

    def create(self, validated_data):
        user = validated_data.get("user")
        if not UserProfile.objects.filter(user=user).exists():
            country = validated_data.get("country_id")
            city = validated_data.get("city_id")
            if country:
                validated_data["country_id"] = country.pk
            if city:
                validated_data["city_id"] = city.pk
            user_profile = UserProfile.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("This user already has a profile")

        return user_profile

    def update(self, instance, validated_data):
        instance.country = validated_data.get("country_id")
        instance.city = validated_data.get("city_id")
        instance.telegram = validated_data.get("telegram", instance.telegram)
        instance.instagram = validated_data.get("instagram", instance.instagram)
        instance.facebook = validated_data.get("facebook", instance.facebook)
        instance.linkedin = validated_data.get("linkedin", instance.linkedin)

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

    def validate_username(self, value, field_name):
        if value is not None:
            pattern = r"^[a-zA-Z0-9_.-@!#$%^&*()<>/?|}{~:]*$"
            if not re.match(pattern, value):
                raise serializers.ValidationError(
                    f"{field_name} username can only contain latin letters, numbers, special symbols"
                )
        return value

    def validate_telegram(self, value):
        return self.validate_username(value, "Telegram")

    def validate_instagram(self, value):
        return self.validate_username(value, "Instagram")

    def validate_facebook(self, value):
        return self.validate_username(value, "Facebook")

    def validate_linkedin(self, value):
        return self.validate_username(value, "LinkedIn")
