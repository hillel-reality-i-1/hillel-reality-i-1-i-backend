import django_filters
from ..models import Post


class PostFilter(django_filters.FilterSet):
    all_countries = django_filters.BooleanFilter(method="filter_all_countries", label="All counties")

    def filter_all_countries(self, queryset, name, value):
        if value:
            return queryset.filter(country__isnull=False)
        return queryset

    class Meta:
        model = Post
        fields = {
            "country": ["exact"],
            "creation_date": ["gte", "lte"],
            "professional_tags": ["exact"],
        }
