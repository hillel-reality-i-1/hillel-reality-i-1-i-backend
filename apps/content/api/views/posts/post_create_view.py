from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.content.models import Post
from apps.content.api.serializers import PostSerializer
from apps.content.utils.aws_utils import moderation_image_with_aws, moderate_img
from apps.users.permissions import IsVerifiedUser


class PostCreateView(CreateAPIView):
    # Раскоментировать если для создания постов нужен вериф. номер телефона
    # permission_classes = [IsAuthenticated, IsUserPhoneVerif]
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if serializer.data.get("image_to_post"):
            path = serializer.data.get("image_to_post").split("/")
            path = "/".join(path[1:])
            response = moderation_image_with_aws(path)
            moderate_img(Post, response, path, serializer, None, None, "post_image")

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

        user_profile = self.request.user.userprofile
        user_profile.last_posts.add(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
