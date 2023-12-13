from django.db import models
from apps.expert.models import Profession, Service
from apps.users.models import User


class UserProfileExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.username}'s extended user profile"
