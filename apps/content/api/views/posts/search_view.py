from json import JSONDecodeError
from cities_light.models import Country
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from rest_framework import generics
from rest_framework import serializers
from apps.content.api.serializers import PostSerializer
from apps.content.models import Post
from apps.expert.models import Category
import json
from rest_framework.permissions import AllowAny
from apps.content.api.paginations import TenHundredPagination


class SearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = TenHundredPagination

    @staticmethod
    def validate_query_data(query_data):
        if query_data["query"]:
            if not (2 <= len(query_data["query"]) <= 100):
                raise serializers.ValidationError(
                    {"query": "The query parameter must be between 2 and 100 characters long."}
                )
            if not isinstance(query_data["query"], str):
                raise serializers.ValidationError({"query": "The query parameter must be a string."})

        try:
            if query_data["countries_id"]:
                query_data["countries_id"] = list(json.loads(query_data["countries_id"]))
        except (TypeError, JSONDecodeError):
            raise serializers.ValidationError({"country_id": "The country_ids parameter must be a list of integers."})

        try:
            if query_data["categories_id"]:
                query_data["categories_id"] = list(json.loads(query_data["categories_id"]))
        except (TypeError, JSONDecodeError):
            raise serializers.ValidationError({"category_id": "The category_ids parameter must be a list of integers."})

        return query_data

    @staticmethod
    def get_values(query_data, model, key: str):
        values = list(model.objects.filter(id__in=query_data.get(key)).values_list("name", flat=True))
        if not values:
            raise serializers.ValidationError({f"{key}": f"The specified {key} do not exist in the database."})

        return values

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        countries_id = self.request.GET.get("country_ids", [])
        categories_id = self.request.GET.get("category_ids", [])

        query_data = self.validate_query_data(
            {"query": query, "countries_id": countries_id, "categories_id": categories_id}
        )

        # Checking the availability of search data
        if not query and not countries_id and not categories_id:
            return []

        countries = self.get_values(query_data, Country, "countries_id") if countries_id else None
        categories = self.get_values(query_data, Category, "categories_id") if categories_id else None

        # Search filter for Post
        post_queryset = (
            Post.objects.annotate(
                search=SearchVector("title", "content"),
            )
            .filter(
                Q(search=SearchQuery(query))
                | Q(author__full_name__icontains=query)
                | Q(author__username__icontains=query)
            )
            .distinct()
        )

        # Applying filters
        if countries:
            post_queryset = post_queryset.filter(country__name__in=countries)

        if categories:
            post_queryset = post_queryset.filter(category__name__in=categories)

        return post_queryset.order_by("-creation_date")
