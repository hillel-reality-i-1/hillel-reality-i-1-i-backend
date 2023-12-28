from django.utils import timezone
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.content.models import Post
from apps.content.permissions import IsAuthorOrReadOnly
from apps.content.api.serializers import PostSerializer


class PostModifiedDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
