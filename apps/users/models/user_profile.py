import re

from cities_light.models import Country, City
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework.exceptions import ValidationError

from apps.content.models import Post, Comment
from apps.files.models import Image
from apps.users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import serializers


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=14, null=True, blank=True)
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

    last_posts = models.ManyToManyField(Post, related_name="last_user_posts", blank=True)
    last_comments = models.ManyToManyField(Comment, related_name="last_user_comments", blank=True)
    last_reacted_posts = models.ManyToManyField(Post, related_name="last_reacted_user_posts", blank=True)
    last_contributions = models.ManyToManyField(Comment, related_name="last_user_contributions", blank=True)

    saved_posts = models.ManyToManyField(Post, related_name="saved_posts_by_users", blank=True)

    # Fields for Twilio verification
    twilio_verification_sid = models.CharField(max_length=255, null=True, blank=True)

    email_is_visible = models.BooleanField(default=True)
    phone_is_visible = models.BooleanField(default=True)
    telegram_is_visible = models.BooleanField(default=True)
    instagram_is_visible = models.BooleanField(default=True)
    facebook_is_visible = models.BooleanField(default=True)
    linkedin_is_visible = models.BooleanField(default=True)

    telegram = models.CharField(
        unique=True,
        max_length=50,
        null=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=50)],
    )
    instagram = models.CharField(
        unique=True,
        max_length=50,
        null=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=50)],
    )
    facebook = models.CharField(
        unique=True,
        max_length=200,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(limit_value=200)],
    )
    linkedin = models.CharField(
        unique=True,
        max_length=200,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(limit_value=200)],
    )

    def __str__(self):
        return f"{self.user.username}'s user profile with id {self.pk}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent's __init__ method
        self.set_origins_fields()

    def set_origins_fields(self):
        self._original_telegram = self.telegram
        self._original_instagram = self.instagram
        self._original_facebook = self.facebook
        self._original_linkedin = self.linkedin
        self._original_phone_number = self.phone_number

    def clean(self):
        # Check unique of telegram, instagram, facebook, linkedin
        if self.telegram != self._original_telegram:
            if (
                self.telegram is not None
                and UserProfile.objects.exclude(pk=self.pk).filter(telegram=self.telegram).exists()
            ):
                raise serializers.ValidationError({"telegram": "Such telegram account already exists."})
            else:
                self.validate_telegram(self.telegram)

        if self.instagram != self._original_instagram:
            if (
                self.instagram is not None
                and UserProfile.objects.exclude(pk=self.pk).filter(instagram=self.instagram).exists()
            ):
                raise serializers.ValidationError({"instagram": "Such instagram account already exists."})
            else:
                self.validate_instagram(self.instagram)

        if self.facebook != self._original_facebook:
            if (
                self.facebook is not None
                and UserProfile.objects.exclude(pk=self.pk).filter(facebook=self.facebook).exists()
            ):
                raise serializers.ValidationError({"facebook": "Such facebook account already exists."})
            else:
                self.validate_facebook(self.facebook)

        if self.linkedin != self._original_linkedin:
            if (
                self.linkedin is not None
                and UserProfile.objects.exclude(pk=self.pk).filter(linkedin=self.linkedin).exists()
            ):
                raise serializers.ValidationError({"linkedin": "Such linkedin account already exists."})
            else:
                self.validate_linkedin(self.linkedin)

        if self.phone_number != self._original_phone_number:
            if (
                self.phone_number is not None
                and UserProfile.objects.exclude(pk=self.pk)
                .filter(phone_number=self.phone_number, phone_verified=True)
                .exists()
            ):
                raise serializers.ValidationError({"phone_number": "Such phone_number already verified."})
            else:
                try:
                    if self.phone_number:
                        phone_instance = PhoneNumber.from_string(str(self.phone_number))
                        validate_international_phonenumber(phone_instance)
                except ValidationError as e:
                    raise serializers.ValidationError({"phone_number": str(e)})

        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        self.set_origins_fields()
        super().save(*args, **kwargs)

    @staticmethod
    def validate_social_media_name(value, field_name):
        if value is not None:
            pattern = r"^[a-zA-Z0-9-_.-@!#$%^&*()<>/?|}{~:]*$"

            if not re.match(pattern, value):
                raise serializers.ValidationError(
                    f"{field_name} username can only contain latin letters, numbers, special symbols"
                )
        return value

    def validate_telegram(self, value):
        return self.validate_social_media_name(value, "Telegram")

    def validate_instagram(self, value):
        return self.validate_social_media_name(value, "Instagram")

    def validate_facebook(self, value):
        return self.validate_social_media_name(value, "Facebook")

    def validate_linkedin(self, value):
        return self.validate_social_media_name(value, "LinkedIn")
