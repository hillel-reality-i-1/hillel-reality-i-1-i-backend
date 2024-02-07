from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.content.utils.aws_utils import remove_img_from_disk
from apps.files.api.serializers.image_serializer import image_handle
from apps.files.models import File
from apps.users.models import UserProfileExtended

User = get_user_model()


class PortfolioSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.ImageField(required=True)

    class Meta:
        model = File
        fields = ("id", "author", "file", "creation_date")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = instance.author.username
        return representation

    def create(self, validated_data):
        image_data = validated_data.pop("file")
        processed_image_data = image_handle(image_data)

        if UserProfileExtended.objects.filter(user=validated_data.get("author")).exists():
            if len(File.objects.filter(author=validated_data.get("author"))) < 10:
                # moderate_img(processed_image_data)
                created_image = super().create({**validated_data, "file": processed_image_data})
            else:
                raise serializers.ValidationError("An expert's profile cannot contain more than 10 files.")
        else:
            raise serializers.ValidationError("The user does not have an expert's profile. You can't upload the file")

        return created_image

    def update(self, instance, validated_data):
        image_data = validated_data.pop("file")

        if image_data:
            processed_image_data = image_handle(image_data)
            instance.file = processed_image_data

        instance.save()
        return instance

    def delete(self, instance, **kwargs):
        remove_img_from_disk(str(instance.file))
        instance.delete()

        return instance
