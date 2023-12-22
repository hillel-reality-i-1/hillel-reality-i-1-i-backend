from rest_framework import generics

from ..serializers import CombinedSerializer
from ...models import Post, Comment, Contribution
from rest_framework.response import Response
from rest_framework import status


class DeleteUserContentView(generics.DestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        return {
            'posts': Post.objects.filter(author=user),
            'comments': Comment.objects.filter(author=user),
            'contributions': Contribution.objects.filter(author=user),
        }

    def get_serializer_class(self):
        return CombinedSerializer()

    @staticmethod
    def perform_destroy(instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for _, obj_list in queryset.items():
            for obj in obj_list:
                self.perform_destroy(obj)

        return Response(status=status.HTTP_204_NO_CONTENT)
