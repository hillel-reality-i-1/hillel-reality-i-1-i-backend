import django_filters
from ..models import Post


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'creation_date': ['gte', 'lte'],
            'professional_tags': ['exact'],
        }
