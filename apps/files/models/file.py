from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Here must be path to files from settings
PATH_TO_UPLOAD = 'files/'


class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to=PATH_TO_UPLOAD)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.file_name
