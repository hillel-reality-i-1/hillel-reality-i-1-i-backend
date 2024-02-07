from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.files.models import Image
from apps.users.models import UserProfile

from apps.content.utils.aws_utils import image_handle, remove_img_from_disk

User = get_user_model()


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

            images = Image.objects.filter(author=validated_data.get("author"))
            if images:
                img = Image.objects.get(author=validated_data.get("author"))
                img.image = processed_image_data
                img.save()
                return img

            else:
                created_image = super().create({**validated_data, "image": processed_image_data})
                user_profile = UserProfile.objects.get(user=validated_data.get("author"))
                user_profile.profile_picture = created_image
                user_profile.save()
                return created_image
        else:
            raise serializers.ValidationError("The user does not have a profile. You can't upload the image")

    def update(self, instance, validated_data):
        image_data = validated_data.pop("image")

        if image_data:
            processed_image_data = image_handle(image_data)
            instance.image = processed_image_data

        instance.save()
        return instance

    def delete(self, instance, **kwargs):
        remove_img_from_disk(str(instance.image))
        instance.delete()

        return instance
