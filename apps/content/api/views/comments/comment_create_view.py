from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.content.models import Comment, Post
from apps.users.permissions import IsVerifiedUser
from apps.content.api.serializers import CommentSerializer


class CommentsCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        parent_id = self.request.data.get("parent", None)

        if parent_id:
            parent_comment = Comment.objects.get(pk=parent_id)
            serializer.save(author=self.request.user, post_id=post_id, parent=parent_comment, is_parent=False)
        else:
            post = Post.objects.get(pk=post_id)
            serializer.save(author=self.request.user, post=post)

            user_profile = self.request.user.userprofile
            user_profile.last_comments.add(serializer.instance)
            user_profile.save()
