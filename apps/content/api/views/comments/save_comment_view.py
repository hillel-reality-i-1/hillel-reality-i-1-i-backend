from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import Comment
from apps.users.permissions import IsVerifiedUser


class SaveCommentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        profile = request.user.userprofile
        profile.saved_comments.add(comment)
        return Response({"message": "Коментар успішно збережено в обране."})


class UnsaveCommentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        profile = request.user.userprofile
        profile.saved_comments.remove(comment)
        return Response({"message": "Коментар успішно видалено з обраного."})
