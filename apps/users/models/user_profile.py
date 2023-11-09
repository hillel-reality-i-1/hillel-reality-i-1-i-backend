from django.db import models
from apps.users.models import User


class Country:
    pass


class City:
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    about_my_self = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    # profile_picture = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(upload_to="files/")

    def __str__(self):
        return f"{self.user.username}'s user profile"
