from cities_light.models import Country, City
from rest_framework import serializers
from apps.content.api.serializers import PostSerializer, CommentSerializer, SavedPostSerializer, SavedCommentSerializer
from apps.files.api.serializers import ImageSerializer
from apps.location.serializers.city_serializer import CitySerializerNew
from apps.location.serializers.country_serializer import CountrySerializer
from apps.users.models import UserProfile
from django.db import IntegrityError


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
        # fields = "__all__"
        fields = (
            "id",
            "user",
            "email",
            "full_name",
            "username",
            "profile_picture",
            "country",
            "city",
            "country_id",
            "city_id",
            "telegram",
            "instagram",
            "facebook",
            "linkedin",
            "phone_number",
            "about_my_self",
            "phone_verified",
            "twilio_verification_sid",
            "last_posts",
            "last_comments",
            "last_reacted_posts",
            "last_contributions",
            "saved_posts",
            "saved_comments",
        )
        read_only_fields = (
            "twilio_verification_sid",
            "phone_verified",
            "saved_posts",
            "saved_comments",
            "last_posts",
            "last_comments",
            "last_reacted_posts",
            "last_contributions",
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
        validated_data = self.check_empty_strings(validated_data)

        user = validated_data.pop("user")
        country = validated_data.get("country_id")
        city = validated_data.get("city_id")

        validated_data["country_id"] = country.pk if country else None
        validated_data["city_id"] = city.pk if city else None

        # try:
        #     profile, created = UserProfile.objects.update_or_create(user=user, defaults=validated_data)
        # except IntegrityError:
        #     raise serializers.ValidationError("Unable to create or update profile")
        try:
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                for field, value in validated_data.items():
                    setattr(profile, field, value)
                profile.save(clean=True)
                return profile
            else:
                profile = UserProfile(user=user, **validated_data)
                profile.save(clean=True)
                return profile
        except IntegrityError:
            raise serializers.ValidationError("Unable to create or update profile")

        # return profile

    def update(self, instance, validated_data):
        validated_data = self.check_empty_strings(validated_data)

        instance.country = validated_data.get("country_id")
        instance.city = validated_data.get("city_id")
        instance.telegram = validated_data.get("telegram", instance.telegram)
        instance.instagram = validated_data.get("instagram", instance.instagram)
        instance.facebook = validated_data.get("facebook", instance.facebook)
        instance.linkedin = validated_data.get("linkedin", instance.linkedin)

        new_phone_number = validated_data.get("phone_number")

        if new_phone_number or "phone_number" in list(validated_data.keys()) and validated_data["phone_number"] is None:
            instance.phone_number = new_phone_number if new_phone_number else None
            instance.phone_verified = False
            instance.twilio_verification_sid = None
            instance.phone_verified_request_id = None

        instance.about_my_self = validated_data.get("about_my_self", instance.about_my_self)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)

        instance.save(clean=True)

        return instance

    @staticmethod
    def check_empty_strings(dictionary):
        for key, value in dictionary.items():
            if isinstance(value, str) and value.strip() == "":
                dictionary[key] = None
        return dictionary
