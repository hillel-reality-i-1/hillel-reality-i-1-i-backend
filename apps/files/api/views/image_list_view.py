from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.files.api.serializers import ImageSerializer
from apps.files.models import Image
from apps.users.permissions import IsAdminOrImageOwner


class ImageListView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrImageOwner]
