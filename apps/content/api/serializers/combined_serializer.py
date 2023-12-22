from rest_framework import serializers
from apps.content.api.serializers import PostSerializer, CommentSerializer


class CombinedSerializer(serializers.Serializer):
    post_data = PostSerializer()
    comment_data = CommentSerializer()
