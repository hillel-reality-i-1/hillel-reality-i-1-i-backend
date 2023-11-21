from io import BytesIO
from PIL import Image as PilImg
from rest_framework import serializers
from apps.files.api.serializers import ImageSerializer
from apps.files.models import Image
from apps.users.models import UserProfile
from django.core.files.base import ContentFile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField(read_only=True)
    profile_picture = ImageSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_email(self, obj):
        return self.get_user_email(obj)

    def get_user(self, obj):
        return self.get_user_id(obj)

    def get_profile_picture(self, obj):
        return self.get_user_profile_picture(obj)

    def create(self, validated_data):
        profile_picture_data = validated_data.pop("profile_picture", None)
        user_profile = UserProfile.objects.create(**validated_data)
        if profile_picture_data:
            image_data = self.extract_image_data(profile_picture_data, user_profile.user.pk)
            self.process_image_creation(image_data, user_profile)

        return user_profile

    def update(self, instance, validated_data):
        instance.about_my_self = validated_data.get("about_my_self", instance.about_my_self)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        profile_picture_data = validated_data.get("profile_picture")

        if profile_picture_data:
            image_data = self.extract_image_data(profile_picture_data, instance.user.pk)
            self.process_image_update(instance, image_data)

        instance.save()
        return instance

    def get_user_email(self, obj):
        return obj.user.email if isinstance(obj, UserProfile) else obj.author.email

    def get_user_id(self, obj):
        return obj.user.pk if isinstance(obj, UserProfile) else obj.author.pk

    def get_user_profile_picture(self, obj):
        if isinstance(obj, UserProfile):
            return ImageSerializer(obj.profile_picture).data if obj.profile_picture else None
        elif isinstance(obj, Image):
            return ImageSerializer(obj).data

    def extract_image_data(self, profile_picture_data, author_id):
        img = self.image_handle(profile_picture_data.get("image"))
        return {
            "author": author_id,
            "image_name": profile_picture_data.get("image_name"),
            "image": img,
        }

    def process_image_creation(self, image_data, user_profile):
        image_serializer = ImageSerializer(data=image_data)
        if image_serializer.is_valid():
            image = image_serializer.save()
            user_profile.profile_picture = image
            user_profile.save()
        else:
            raise serializers.ValidationError(image_serializer.errors)

    def process_image_update(self, instance, image_data):
        if instance.profile_picture:
            image_serializer = ImageSerializer(instance.profile_picture, data=image_data)
        else:
            image_serializer = ImageSerializer(data=image_data)

        if image_serializer.is_valid():
            image = image_serializer.save()
            instance.profile_picture = image
        else:
            raise serializers.ValidationError(image_serializer.errors)

    def image_handle(self, image_data):
        image = PilImg.open(image_data)
        if image.format.lower() not in ["jpeg", "png"]:
            raise serializers.ValidationError("Invalid image format. Supported formats: JPEG, PNG.")

        max_size = (320, 240)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size)

        compressed_image_buffer = BytesIO()
        image.save(compressed_image_buffer, format=image.format.upper())

        return ContentFile(compressed_image_buffer.getvalue(), name=image_data.name)
