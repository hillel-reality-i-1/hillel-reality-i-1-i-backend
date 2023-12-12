from rest_framework import viewsets, status
from rest_framework.response import Response

from ...models import Post
from ..serializers import PostSerializer
from ..paginations import TenHundredPagination

from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters

from ...filters import PostFilter
from ...permissions import IsVerifiedAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-creation_date')
    serializer_class = PostSerializer
    pagination_class = TenHundredPagination
    permission_classes = [IsVerifiedAuthorOrReadOnly]
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    filterset_class = PostFilter
    ordering_fields = (
        'professional_tags',
        'creation_date',
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().create(request, *args, **kwargs)
