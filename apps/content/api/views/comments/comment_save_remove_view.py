from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import Comment
from apps.users.permissions import IsVerifiedUser


class SaveRemoveCommentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        profile = request.user.userprofile

        if comment.is_parent:
            if comment in profile.saved_comments.all():
                profile.saved_comments.remove(comment)
                message = "Коментар успішно видалено з обраного."
            else:
                profile.saved_comments.add(comment)
                message = "Коментар успішно збережено в обране."
            return Response({"message": message})
        else:
            raise serializers.ValidationError("Reply не можна зберігати")
