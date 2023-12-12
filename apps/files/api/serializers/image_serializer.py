from shutil import rmtree

from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.files.models import Image
from apps.users.models import UserProfile

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
        created_image = None
        if avatara:
            if UserProfile.objects.filter(user=validated_data.get("author")).exists():
                images = Image.objects.filter(author=validated_data.get("author"))
                if images:
                    for img in images:
                        path = str(img.image)
                        folder_path = path[: path.rfind("/")]
                        try:
                            rmtree(folder_path)
                        except Exception as e:
                            print(f"Error while deleting file {folder_path}: {e}")

                    Image.objects.filter(author=validated_data.get("author")).delete()

                created_image = super().create({**validated_data, "image": processed_image_data})
                user_profile = UserProfile.objects.get(user=validated_data.get("author"))
                user_profile.profile_picture = created_image
                user_profile.save()
            else:
                raise serializers.ValidationError("The user does not have a profile. You can't upload the image")

        return created_image

    def image_handle(self, image_data):
        max_size_bytes = 5 * 1024 * 1024
        if image_data.size > max_size_bytes:
            raise serializers.ValidationError("Image size exceeds the maximum allowed size (5 MB).")

        image = PilImg.open(image_data)
        if image.format.lower() not in ["jpeg", "png"]:
            raise serializers.ValidationError("Invalid image format. Supported formats: JPEG, PNG.")

        max_size = (320, 240)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size)

        compressed_image_buffer = BytesIO()
        image.save(compressed_image_buffer, format=image.format.upper())

        return ContentFile(compressed_image_buffer.getvalue(), name=image_data.name)
