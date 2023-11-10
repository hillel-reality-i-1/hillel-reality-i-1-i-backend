from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...models import Image

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Image
        fields = ('id', 'author', 'image_name', 'image', 'creation_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username
        return representation
