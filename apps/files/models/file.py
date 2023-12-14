from django.db import models
from django.contrib.auth import get_user_model

from apps.files.models.image import universal_file_path_builder

User = get_user_model()


class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # file_name = models.CharField(max_length=100)
    file = models.ImageField(upload_to=universal_file_path_builder, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        path = str(self.file)
        label = path.rfind("/")
        return path[label - 64 : label]
