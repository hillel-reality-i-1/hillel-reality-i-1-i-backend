from rest_framework import serializers

from apps.content.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username", read_only=True)
    replies = serializers.SerializerMethodField()
    is_parent = serializers.BooleanField(read_only=True)
    helpful_count = serializers.IntegerField(read_only=True)
    not_helpful_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "text",
            "helpful_count",
            "not_helpful_count",
            "creation_date",
            "updated_date",
            "replies",
            "is_parent",
        ]
        read_only_fields = ["post", "helpful_count", "not_helpful_count"]

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not instance.is_parent:
            representation.pop("helpful_count", None)
            representation.pop("not_helpful_count", None)

        return representation
