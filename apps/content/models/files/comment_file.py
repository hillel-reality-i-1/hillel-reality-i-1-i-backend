from django.db import models
from ..comment import Comment
from apps.files.models import File


class CommentFile(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
