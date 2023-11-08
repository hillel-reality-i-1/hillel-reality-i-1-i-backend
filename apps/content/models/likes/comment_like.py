from django.db import models
from django.contrib.auth import get_user_model
from ..comment import Comment

User = get_user_model()


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
