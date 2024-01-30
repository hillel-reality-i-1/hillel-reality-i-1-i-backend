from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import get_language
from apps.files.models.post_image import PostImage

from .reaction_serializer import ReactionSerializer
from .comment_serializer import CommentSerializer
from ...models import Post, Comment
from ...utils.aws_utils import image_handle, remove_img_from_disk, save_moderate_img

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    content = serializers.CharField(min_length=100, max_length=10000)
    post_image = serializers.ImageField(required=False)
    reactions = ReactionSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    contributions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "category",
            "country",
            "content",
            "reactions",
            "creation_date",
            "comments",
            "contributions",
            "post_image",
        ]
        read_only_fields = ["author"]

    def get_comments(self, obj):
        root_comments = Comment.objects.filter(post=obj, parent=None)

        serializer = CommentSerializer(root_comments, many=True)
        return serializer.data

    def get_contributions(self, obj):
        contributions = Comment.objects.filter(post=obj, parent=None, is_contribution=True)

        serializer = CommentSerializer(contributions, many=True)
        return serializer.data

    def validate_category(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("Ви можете додати до 3 категорій")
        return value

    def validate_country(self, value):
        try:
            if len(value) > 5:
                raise serializers.ValidationError("Ви можете обраті не більше 4 країн")
            return value
        except TypeError:
            raise serializers.ValidationError("Некоректні дані для країни")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        language = get_language()
        representation["country"] = [
            country.alternate_names if language != "en" else country.name for country in instance.country.all()
        ]
        representation["category"] = [category.name for category in instance.category.all()]
        if hasattr(instance, "postimage") and instance.postimage:
            representation["image_to_post"] = str(instance.postimage.post_image.url)
        else:
            representation["image_to_post"] = None

        return representation

    def create(self, validated_data):
        post_image_data = validated_data.pop("post_image", None)
        processed_image_data = None

        if post_image_data:
            processed_image_data = image_handle(post_image_data)
            save_moderate_img(processed_image_data)

        post = super().create(validated_data)
        if processed_image_data:
            PostImage.objects.create(post_image=processed_image_data, post=post)

        return post

    def update(self, instance, validated_data):
        post_image_data = validated_data.pop("post_image", None)

        if post_image_data:
            processed_image_data = image_handle(post_image_data)
            save_moderate_img(processed_image_data)

            if hasattr(instance, "postimage") and instance.postimage:
                remove_img_from_disk(str(instance.postimage.post_image))
                instance.postimage.delete()

            post_image = PostImage.objects.create(post_image=processed_image_data, post=instance)
            instance.postimage = post_image

        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.category.set(validated_data.get("category", instance.category))
        instance.country.set(validated_data.get("country", instance.country))

        instance.save()
        return instance

    def delete(self, instance, **kwargs):
        if hasattr(instance, "postimage") and instance.postimage:
            remove_img_from_disk(str(instance.postimage.post_image))
        instance.delete()

        return instance
