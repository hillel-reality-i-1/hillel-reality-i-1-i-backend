from rest_framework import viewsets

from ...models import Article
from ..serializers import ArticleSerializer
from ..paginations import TenHundredPagination

from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters

from ...filters import ArticleFilter


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = TenHundredPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    filterset_class = ArticleFilter
    ordering_fields = (
        'professional_tags',
        'creation_date',
    )
