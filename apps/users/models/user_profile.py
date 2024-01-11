from cities_light.models import Country, City
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from apps.content.models import Post, Comment
from apps.files.models import Image
from apps.users.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)
    about_my_self = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=500)],
    )
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)

    saved_posts = models.ManyToManyField(Post, related_name="saved_posts_by_users", blank=True)
    saved_comments = models.ManyToManyField(Comment, related_name="saved_comments_by_users", blank=True)

    # Fields for Twilio verification
    twilio_verification_sid = models.CharField(max_length=255, null=True, blank=True)

    telegram = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=50)],
    )
    instagram = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=50)],
    )
    facebook = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(limit_value=200)],
    )
    linkedin = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(limit_value=200)],
    )

    def __str__(self):
        return f"{self.user.username}'s user profile with id {self.pk}"
