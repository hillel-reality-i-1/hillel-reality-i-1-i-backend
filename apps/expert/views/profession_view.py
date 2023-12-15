from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Profession
from ..serializers import ProfessionSerializer


class ProfessionListView(APIView):
    def get(self, request):
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(professions, many=True)
        return Response(serializer.data)


@extend_schema(request=ProfessionSerializer, responses={201: None})
class ProfessionCreateView(APIView):
    serializer_class = ProfessionSerializer

    def post(self, request):
        custom_profession_name = request.data.get("name")

        if custom_profession_name:
            custom_profession, created = Profession.objects.get_or_create(name=custom_profession_name)

            if created:
                serializer = ProfessionSerializer(custom_profession)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Профессия уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Не указано имя профессии"}, status=status.HTTP_400_BAD_REQUEST)
