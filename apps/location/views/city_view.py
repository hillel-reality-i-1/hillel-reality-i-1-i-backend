from rest_framework import viewsets

# from rest_framework.views import APIView
# from rest_framework.response import Response
from cities_light.models import City

# from apps.content.api.paginations import ThreeHundredPagination
# from apps.content.api.paginations.three_hundred_pagination import CityPagination
# from apps.location.serializers.city_serializer import CitySerializer
from apps.users.serializers.user_profile_serializer import CitySerializerNew


# class CityListView(APIView):
#     def get(self, request):
#         cities = City.objects.all()
#         serializer = CitySerializer(cities, many=True)
#         return Response(serializer.data)


class CityListView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializerNew
    # pagination_class = CityPagination
