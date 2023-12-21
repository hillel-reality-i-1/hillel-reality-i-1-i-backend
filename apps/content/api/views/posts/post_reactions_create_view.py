from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsVerifiedUser
from apps.content.api.serializers import PostSerializer, ReactionSerializer
from apps.content.models import Post
from apps.content.models.reaction import Reaction


class PostReactionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    serializer_class = ReactionSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        user = self.request.user
        reaction_type = request.data.get("reaction_type")

        with transaction.atomic():
            existing_reaction = Reaction.objects.select_for_update().filter(user=user, post=post).first()

            if existing_reaction:
                if existing_reaction.reaction_type == reaction_type:
                    existing_reaction.delete()
                    return Response({"detail": "Рекція видалена"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    existing_reaction.delete()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, post=post)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
