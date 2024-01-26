from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import Post
from apps.users.permissions import IsVerifiedUser


class SaveRemovePostAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        profile = request.user.userprofile

        if post in profile.saved_posts.all():
            profile.saved_posts.remove(post)
            return Response({"detail": "Допіс успишно видалено з обраного"})

        profile.saved_posts.add(post)
        return Response({"message": "Допис успішно додано в обране."})
