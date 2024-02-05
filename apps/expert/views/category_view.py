from rest_framework.response import Response
from rest_framework.views import APIView

from apps.expert.models import Category
from apps.expert.serializers import CategorySerializer


class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all()

        other_category = categories.filter(name="Інше").first()

        if not other_category:
            other_category = Category.objects.create(name="Інше")

        sorted_categories = list(categories.exclude(name="Інше")) + [other_category]

        serializer = CategorySerializer(sorted_categories, many=True)
        return Response(serializer.data)
