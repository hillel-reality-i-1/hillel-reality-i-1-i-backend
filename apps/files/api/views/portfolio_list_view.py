from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.files.api.serializers.porfolio_serializer import PortfolioSerializer
from apps.files.models import File
from apps.users.permissions import IsAdminOrPortfolioOwner


class PortfolioListView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPortfolioOwner]
