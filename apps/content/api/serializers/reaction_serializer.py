from rest_framework import serializers

from apps.content.models.reaction import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = Reaction
        fields = ["id", "reaction_type", "user_username"]

    def get_user_username(self, obj):
        return obj.user.username
