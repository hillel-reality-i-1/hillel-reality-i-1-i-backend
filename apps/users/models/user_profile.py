from cities_light.models import Country, City
from django.db import models
from apps.files.models import Image
from apps.users.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # phone_number = models.CharField(max_length=15)
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)
    about_my_self = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    # profile_picture = models.ImageField(upload_to="files/")
    profile_picture = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)

    # Fields for Twilio verification
    twilio_phone_verified = models.BooleanField(default=False)
    twilio_verification_sid = models.CharField(max_length=255, null=True, blank=True)

    # Fields for Vonage(nexmo) verification
    phone_verified = models.BooleanField(default=False)
    phone_verified_request_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s user profile"
