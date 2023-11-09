from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Profession
from ..serializers import ProfessionSerializer


class ProfessionListView(APIView):
    def get(self, request):
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(professions, many=True)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     custom_profession_name = request.data.get('custom_profession_name')
    #
    #     if custom_profession_name:
    #         custom_profession, created = Profession.objects.get_or_create(name=custom_profession_name)
    #         serializer = self.get_serializer(custom_profession)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #     return Response({'detail': 'Custom profession name not provided'}, status=status.HTTP_400_BAD_REQUEST)
