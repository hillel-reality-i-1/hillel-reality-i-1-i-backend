from django.db import models
from django.contrib.auth import get_user_model
from .post import Post
from apps.files.models import Image

User = get_user_model()


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    images = models.ManyToManyField(Image, related_name='comment_images', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author}. Created at {self.creation_date}'

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def get_images(self):
        return self.images.all()
