from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.files.api.serializers import ImageSerializer
from .reaction_serializer import ReactionSerializer
from .comment_serializer import CommentSerializer
from ...models import Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    content = serializers.CharField(min_length=100, max_length=10000)
    images = ImageSerializer(many=True, required=False)
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
            "images",
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

    def validate_professional_tags(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("Ви можете додати до 3 професийніх галузей")
        return value

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
        representation["country"] = [country.name for country in instance.country.all()]
        representation["category"] = [category.name for category in instance.category.all()]
        return representation
