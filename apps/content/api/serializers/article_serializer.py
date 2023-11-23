from rest_framework import serializers
from apps.files.api.serializers import ImageSerializer
from apps.expert.serializers import ProfessionSerializer
from django.contrib.auth import get_user_model
from ...models import Article

User = get_user_model()


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    professional_tags = ProfessionSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            'id', 'author', 'title', 'content', 'likes', 'dislikes', 'images', 'professional_tags', 'creation_date'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_likes'] = instance.total_likes()
        representation['total_dislikes'] = instance.total_dislikes()
        representation['image_urls'] = [image.image.url for image in instance.get_images()]
        representation['professional_tags_names'] = [tag.name for tag in instance.get_professional_tags()]
        return representation
