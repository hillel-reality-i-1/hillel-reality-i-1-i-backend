from rest_framework import viewsets

# from rest_framework.views import APIView
# from rest_framework.response import Response
from cities_light.models import Country
from apps.users.serializers.country_serializer import CountrySerializer


# class CountryListView(APIView):
#     def get(self, request):
#         countries = Country.objects.all()
#         serializer = CountrySerializer(countries, many=True)
#         return Response(serializer.data)


class CountryListView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
