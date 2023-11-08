from django.db import models
from ..comment import Comment
from apps.files.models import Image


class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
