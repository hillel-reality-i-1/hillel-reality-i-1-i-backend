from rest_framework import serializers

from apps.content.utils.aws_utils import remove_img_from_disk
from apps.files.models.post_image import PostImage


class PostImageSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    post_image = serializers.ImageField(required=True)

    class Meta:
        model = PostImage
        fields = ("id", "post", "post_image", "creation_date")

    def delete(self, instance, **kwargs):
        remove_img_from_disk(str(instance.post_image))
        instance.delete()

        return instance
