from django.db import models
from ..article import Article
from apps.files.models import File


class ArticleFile(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
