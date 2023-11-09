from django.db import models
from ..article import Article
from apps.files.models import Image


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
