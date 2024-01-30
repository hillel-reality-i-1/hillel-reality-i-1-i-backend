from rest_framework import serializers

from apps.content.models import Post


class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "country",
            "content",
            "reactions",
            "creation_date",
        ]
