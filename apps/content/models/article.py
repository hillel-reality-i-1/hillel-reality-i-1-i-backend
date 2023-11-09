from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Article {self.title} by {self.author}. Created at {self.creation_date}'
