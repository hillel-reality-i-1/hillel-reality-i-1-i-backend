from rest_framework.response import Response
from rest_framework.views import APIView

from apps.expert.models import Category
from apps.expert.serializers import CategorySerializer


class CategoryListView(APIView):

    def get(self, request):
        professions = Category.objects.all()
        serializer = CategorySerializer(professions, many=True)
        return Response(serializer.data)
