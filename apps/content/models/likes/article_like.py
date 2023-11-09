from django.db import models
from django.contrib.auth import get_user_model
from ..article import Article

User = get_user_model()


class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
