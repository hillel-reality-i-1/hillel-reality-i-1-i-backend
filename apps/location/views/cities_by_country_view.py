from cities_light.models import City
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import get_language
from apps.location.serializers.city_serializer import CitySerializer


class CitiesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        country_id = serializer.validated_data.get("country")

        cache_key = "cities_all" if country_id is None else f"cities_by_country_{country_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response({"status": "success", "data": cached_data}, status=200)

        language = get_language()

        if country_id is None:
            cities_list = (
                list(City.objects.all().order_by("alternate_names"))
                if language != "en"
                else list(City.objects.all().order_by("name"))
            )
        else:
            cities_list = (
                list(City.objects.filter(country=country_id).order_by("alternate_names"))
                if language != "en"
                else list(City.objects.filter(country=country_id).order_by("name"))
            )

        cities_dict = {
            city.id: {"name": city.alternate_names if language != "en" else city.name, "country": city.country.id}
            for city in cities_list
        }

        cache.set(cache_key, cities_dict)

        return Response({"status": "success", "data": cities_dict}, status=200)
