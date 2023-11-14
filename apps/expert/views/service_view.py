from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Service
from ..serializers import ServiceSerializer


class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServiceCreateView(APIView):
    def post(self, request):
        custom_service_name = request.data.get("name")

        if custom_service_name:
            custom_service, created = Service.objects.get_or_create(name=custom_service_name)

            if created:
                serializer = ServiceSerializer(custom_service)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Профессия уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Не указано имя профессии"}, status=status.HTTP_400_BAD_REQUEST)
