from rest_framework import viewsets

# from rest_framework.views import APIView
# from rest_framework.response import Response
from cities_light.models import City

# from apps.content.api.paginations import ThreeHundredPagination
from apps.content.api.paginations.three_hundred_pagination import CityPagination
from apps.users.serializers.city_serializer import CitySerializer


# class CityListView(APIView):
#     def get(self, request):
#         cities = City.objects.all()
#         serializer = CitySerializer(cities, many=True)
#         return Response(serializer.data)


class CityListView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = CityPagination
