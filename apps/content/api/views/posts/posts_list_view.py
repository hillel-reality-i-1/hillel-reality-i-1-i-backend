from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework import filters as rest_framework_filters
from django_filters import rest_framework as filters

from apps.content.models import Post
from apps.content.filters import PostFilter
from apps.content.api.serializers import PostSerializer
from apps.content.api.paginations import TenHundredPagination


class PostListView(ListAPIView):
    permission_classes = [AllowAny]

    queryset = Post.objects.all().order_by("-creation_date")
    serializer_class = PostSerializer
    pagination_class = TenHundredPagination

    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    filterset_class = PostFilter
    ordering_fields = ("creation_date",)

    def filter_queryset(self, queryset):
        all_countries = self.request.query_params.get("all_countries")
        countries = self.request.query_params.getlist("country")
        if all_countries and all_countries.lower() == "true":
            return queryset
        elif countries:
            return queryset.filter(country__in=countries)
        else:
            return queryset
