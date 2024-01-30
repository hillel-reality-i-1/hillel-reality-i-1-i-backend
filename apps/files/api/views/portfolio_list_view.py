from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
