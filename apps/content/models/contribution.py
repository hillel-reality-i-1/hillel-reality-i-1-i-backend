from django.db import models
from django.contrib.auth import get_user_model
from .article import Article

User = get_user_model()


class Contribution(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author}. Created at {self.creation_date}'
