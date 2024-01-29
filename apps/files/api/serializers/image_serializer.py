from django.core.files.temp import NamedTemporaryFile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.settings import env
from apps.files.models import Image
from apps.users.models import UserProfile

from apps.content.utils.aws_utils import moderation_image_with_aws, image_handle, remove_img_from_disk

User = get_user_model()
TEMP_FILES_PATH = env.str("TEMP_FILES_PATH")


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = Image
        fields = ("id", "author", "image", "creation_date")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = instance.author.username
        return representation

    def create(self, validated_data):
        if UserProfile.objects.filter(user=validated_data.get("author")).exists():
            image_data = validated_data.pop("image")
            processed_image_data = image_handle(image_data)

            with NamedTemporaryFile(delete=True, suffix=".jpg", dir=TEMP_FILES_PATH) as temp_file:
                temp_file.write(processed_image_data.read())
                temporary_path = temp_file.name
                moderation_image_with_aws(temporary_path, serializers)

            images = Image.objects.filter(author=validated_data.get("author"))
            if images:
                for img in images:
                    remove_img_from_disk(str(img.image))

                Image.objects.filter(author=validated_data.get("author")).delete()

            created_image = super().create({**validated_data, "image": processed_image_data})
            user_profile = UserProfile.objects.get(user=validated_data.get("author"))
            user_profile.profile_picture = created_image
            user_profile.save()
        else:
            raise serializers.ValidationError("The user does not have a profile. You can't upload the image")

        return created_image
