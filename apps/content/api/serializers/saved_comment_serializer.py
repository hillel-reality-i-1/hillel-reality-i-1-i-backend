from rest_framework import serializers

from apps.content.models import Comment


class SavedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["post", "helpful_count", "not_helpful_count", "is_parent"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not instance.is_parent:
            representation.pop("helpful_count", None)
            representation.pop("not_helpful_count", None)

        return representation
