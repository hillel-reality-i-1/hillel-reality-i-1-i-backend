from django.db import models

from apps.content.models import Post
from apps.files.models.image import universal_file_path_builder


class PostImage(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null=True)
    post_image = models.ImageField(upload_to=universal_file_path_builder, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post_image)
