import django_filters
from ..models import Post


class PostFilter(django_filters.FilterSet):
    all_countries = django_filters.BooleanFilter(method="filter_all_countries", label="All counties")

    class Meta:
        model = Post
        fields = {
            "country": ["exact"],
            "creation_date": ["gte", "lte"],
            "professional_tags": ["exact"],
        }
