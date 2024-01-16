from rest_framework import viewsets
from django.utils.translation import get_language
from cities_light.models import City

from apps.location.serializers.city_serializer import CitySerializerNew


class CityListView(viewsets.ModelViewSet):
    serializer_class = CitySerializerNew
    # pagination_class = CityPagination

    def get_queryset(self):
        language = get_language()
        return (
            City.objects.all().order_by("alternate_names") if language != "en" else City.objects.all().order_by("name")
        )
