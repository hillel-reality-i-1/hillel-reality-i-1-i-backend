from cities_light.models import City
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.location.serializers.city_serializer import CitySerializer


class CitiesAPIView(APIView):

    def get(self, request, *args, **kwargs):

        serializer = CitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        country_id = serializer.validated_data.get('country')

        cache_key = f'cities_all' if country_id is None else f'cities_by_country_{country_id}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response({'status': 'success', 'data': cached_data}, status=200)

        if country_id is None:
            cities = list(City.objects.all())
        else:
            cities = list(City.objects.filter(country_id=country_id))

        serializer = CitySerializer(cities, many=True)

        cache.set(cache_key, serializer.data)

        return Response({'status': 'success', 'data': serializer.data}, status=200)
