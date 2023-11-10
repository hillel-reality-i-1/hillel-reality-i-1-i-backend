import django_filters
from ..models import Article


class ArticleFilter(django_filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'author': ['exact'],
            'creation_date': ['gte', 'lte'],
            'professional_tags': ['exact'],
        }
