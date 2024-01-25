from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.files.api.serializers.porfolio_serializer import PortfolioSerializer
from apps.files.models import File
from apps.users.permissions import IsAdminOrPortfolioOwner


class PortfolioListView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = File.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPortfolioOwner]
