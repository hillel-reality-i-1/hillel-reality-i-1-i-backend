from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.models import Post
from apps.content.api.serializers import PostSerializer
from apps.users.permissions import IsVerifiedUser


class PostCreateView(CreateAPIView):
    # Раскоментировать если для создания постов нужен вериф. номер телефона
    # permission_classes = [IsAuthenticated, IsUserPhoneVerif]
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
