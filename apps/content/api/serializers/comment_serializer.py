from rest_framework import serializers
from ...models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "text", "creation_date", "updated_date", "replies"]
        read_only_fields = ["post"]

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data
