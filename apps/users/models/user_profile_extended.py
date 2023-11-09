from django.db import models
from apps.expert.models import Profession, Service
from apps.files.models import File
from apps.users.models import User


class UserProfileExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_my_self_ext = models.TextField(null=True, blank=True)
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    # resume = models.FileField(upload_to="files/")
    resume = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}'s extended user profile"
