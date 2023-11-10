from rest_framework import viewsets

from ...models import Comment
from ..serializers import CommentSerializer
from ..paginations import ThreeHundredPagination

from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters

from ...filters import CommentFilter


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = ThreeHundredPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    filterset_class = CommentFilter
    ordering_fields = (
        'creation_date',
    )
