from rest_framework import serializers

from apps.content.models import Contribution


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = "__all__"
        read_only_fields = ["helpful_count"]
