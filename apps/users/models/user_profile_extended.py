from django.db import models
from apps.expert.models import Profession, Service
from apps.users.models import User


class UserProfileExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.ManyToManyField(Profession, blank=True)
    service = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return f"{self.user.username}'s extended user profile with id {self.pk}"
