from cities_light.models import Country
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from rest_framework import generics
from rest_framework import serializers
from apps.content.api.serializers import PostSerializer
from apps.content.models import Post
from apps.expert.models import Category


class SearchView(generics.ListAPIView):
    serializer_class = PostSerializer

    @staticmethod
    def validate_query_data(query_data):
        if not isinstance(query_data["query"], str):
            raise serializers.ValidationError({"query": "The query parameter must be a string."})

        try:
            for i in range(len(query_data["countries_id"])):
                query_data["countries_id"][i] = int(query_data["countries_id"][i])
        except Exception:
            raise serializers.ValidationError({"country_id": "The country_id parameter must be a list of integers."})

        try:
            for i in range(len(query_data["categories_id"])):
                query_data["categories_id"][i] = int(query_data["categories_id"][i])
        except Exception:
            raise serializers.ValidationError({"category_id": "The category_id parameter must be a list of integers."})

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        countries_id = self.request.GET.getlist("country_id", [])
        categories_id = self.request.GET.getlist("category_id", [])

        self.validate_query_data({"query": query, "countries_id": countries_id, "categories_id": categories_id})

        # Checking the availability of search data
        if not query and not countries_id and not categories_id:
            return []

        if countries_id:
            countries = list(Country.objects.filter(id__in=countries_id).values_list("name", flat=True))
        else:
            countries = None
        if categories_id:
            categories = list(Category.objects.filter(id__in=categories_id).values_list("name", flat=True))
        else:
            categories = None

        # Search filter for Post
        post_queryset = (
            Post.objects.annotate(
                search=SearchVector("title", "content"),
            )
            .filter(Q(search=SearchQuery(query)) | Q(author__full_name__icontains=query))
            .distinct()
        )

        # Applying filters
        if countries:
            post_queryset = post_queryset.filter(country__name__in=countries)

        if categories:
            post_queryset = post_queryset.filter(category__name__in=categories)

        return post_queryset
