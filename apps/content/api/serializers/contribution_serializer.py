from rest_framework import serializers
from ...models import Contribution


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ('id', 'text', 'author', 'article', 'creation_date')
