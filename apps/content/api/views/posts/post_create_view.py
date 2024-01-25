from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        post = serializer.save(author=self.request.user)

        user_profile = self.request.user.userprofile
        user_profile.last_posts.add(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
