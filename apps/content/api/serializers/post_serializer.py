from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.files.api.serializers import ImageSerializer
from .reaction_serializer import ReactionSerializer
from .comment_serializer import CommentSerializer
from ...models import Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username", read_only=True)
    title = serializers.CharField(min_length=2, max_length=100)
    content = serializers.CharField(min_length=100, max_length=10000)
    images = ImageSerializer(many=True, required=False)
    reactions = ReactionSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "country",
            "content",
            "professional_tags",
            "images",
            "creation_date",
            "comments",
            "reactions",
        ]

    def get_comments(self, obj):
        root_comments = Comment.objects.filter(post=obj, parent=None)

        serializer = CommentSerializer(root_comments, many=True)
        return serializer.data

    def validate_professional_tags(self, value):
        print(value)
        if len(value) > 3:
            raise serializers.ValidationError("Ви можете додати до 3 професийніх галузей")
        return value

    def validate_country(self, value):
        try:
            if len(value) > 5:
                raise serializers.ValidationError("Ви можете обраті не більше 5 країн")
            return value
        except TypeError:
            raise serializers.ValidationError("Некоректні дані для країни")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["country"] = [country.name for country in instance.country.all()]
        representation["professional_tags"] = [tag.name for tag in instance.professional_tags.all()]
        return representation
