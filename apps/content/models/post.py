from django.db import models
from django.contrib.auth import get_user_model
from apps.files.models import Image
from apps.expert.models import Profession

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='article_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='article_dislikes', blank=True)
    images = models.ManyToManyField(Image, related_name='article_images', blank=True)
    professional_tags = models.ManyToManyField(Profession, related_name='professional_tags', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Article {self.title} by {self.author}. Created at {self.creation_date}'

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def get_images(self):
        return self.images.all()

    def get_professional_tags(self):
        return self.professional_tags.all()
