from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from apps.content.models import Post
from apps.content.permissions import IsAuthorOrReadOnly
from apps.content.api.serializers import PostSerializer
from apps.content.utils.aws_utils import moderation_image_with_aws, moderate_img
from apps.files.models.post_image import PostImage


class PostModifiedView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthorOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        current_post = self.get_object()
        prev_post_image, prev_post_image_path = None, None

        old_post_data = {
            "title": current_post.title,
            "content": current_post.content,
            "category": list(current_post.category.all()),
            "country": list(current_post.country.all()),
        }

        if hasattr(current_post, "postimage") and current_post.postimage and request.data.get("post_image"):
            prev_post_image = PostImage.objects.filter(post=current_post).first()
            prev_post_image_path = prev_post_image.post_image.url.split("/")
            prev_post_image_path = "/".join(prev_post_image_path[1:])

        serializer = self.get_serializer(current_post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if serializer.data.get("image_to_post"):
            path = serializer.data.get("image_to_post").split("/")
            path = "/".join(path[1:])
            response = moderation_image_with_aws(path)
            moderate_img(
                Post,
                response,
                path,
                serializer,
                prev_post_image,
                prev_post_image_path,
                "post_image",
                old_post_data=old_post_data,
            )

        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        post = self.get_object()

        if post.comments.exists():
            raise serializers.ValidationError("Ви не можете редагувати запис із коментарями")
        elif post.reactions.exists():
            raise serializers.ValidationError("Ви не можете редагувати запис із реакціями")

        elapsed_time = timezone.now() - post.creation_date
        if elapsed_time.seconds < 900:
            serializer.save()
        else:
            raise serializers.ValidationError("Ви можете редагувати тільки протягом перших 15 хвилин після створення.")
