from django.db import models

from apps.users.models import User
from apps.content.models import Article, Comment, Contribution


class Complaint(models.Model):
    complaint_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    complaint_article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True)
    complaint_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True)
    complaint_contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE, blank=True)
