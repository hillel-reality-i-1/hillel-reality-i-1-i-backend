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
            "category": ["exact"],
        }

    def filter_all_countries(self, queryset, name, value):
        if value:
            return queryset
        else:
            return queryset.filter(country__isnull=False)
