from rest_framework import viewsets
from django.utils.translation import get_language
from cities_light.models import Country
from apps.location.serializers.country_serializer import CountrySerializer


class CountryListView(viewsets.ModelViewSet):
    # queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        language = get_language()
        return (
            Country.objects.all().order_by("alternate_names")
            if language != "en"
            else Country.objects.all().order_by("name")
        )
