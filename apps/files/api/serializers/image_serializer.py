from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.models import UserProfile
from ...models import Image
from io import BytesIO
from PIL import Image as PilImg
from django.core.files.base import ContentFile

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = ("id", "author", "image", "creation_date")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = instance.author.username
        return representation

    def create(self, validated_data):
        avatara = None
        if validated_data.get("avatara"):
            avatara = validated_data.pop("avatara")
        image_data = validated_data.pop("image")
        processed_image_data = self.image_handle(image_data)

        created_image = super().create({**validated_data, "image": processed_image_data})
        if avatara:
            user_profile = UserProfile.objects.get(user=validated_data.get("author"))
            user_profile.profile_picture = created_image
            user_profile.save()

        return created_image

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
