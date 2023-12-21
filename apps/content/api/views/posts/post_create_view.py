from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.models import Post
from apps.content.permissions import IsUserPhoneVerif
from apps.content.api.serializers import PostSerializer


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsUserPhoneVerif]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
