from random import randint
import re

from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from allauth.account.models import EmailAddress
from django.db import models
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Потрібно вказати email")
        if not password:
            raise ValueError("Потрібно встановити пароль")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.date_joined = timezone.now()
        full_name = extra_fields.get("full_name", "")
        username = self.generate_unique_username(full_name)
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, full_name=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if full_name is None:
            full_name = getattr(settings, "DJANGO_SUPERUSER_FULLNAME", "Super User")
        if email is None:
            email = getattr(settings, "DJANGO_SUPERUSER_EMAIL", "django@gjan.go")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, full_name=full_name, **extra_fields)

    @staticmethod
    def is_username_unique(username):
        return not get_user_model().objects.filter(username=username).exists()

    def generate_unique_username(self, full_name):
        full_name = full_name.replace(" ", "_")
        username = f"{full_name.lower()}_{randint(1, 99999)}"

        if not User.objects.count():
            return f"{full_name.lower()}_{randint(1, 99999)}"

        while not self.is_username_unique(username):
            username = f"{full_name.lower()}_{randint(1, 99999)}"

        return username

    @staticmethod
    def validate_user_username(user):
        if user.username is None:
            return False

        # Length validation
        # if len(user.username) > 32:
        #     raise serializers.ValidationError("Username can be up to 32 characters long")

        # Characters validation
        pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$")
        if not pattern.match(user.username):
            raise serializers.ValidationError(
                "Username can contain Latin letters, numbers, and underscores. Username cannot contain spaces."
                "Username must start with a letter and can't end with an underscore."
            )

        # pattern = rf'\A({user.first_name.lower()}_{user.last_name.lower() if user.last_name else ""}_\d{{1,5}})\Z'
        pattern = rf"\A({user.full_name.lower()}_\d{{1,5}})\Z"
        mo = re.compile(pattern).match(user.username.lower())
        return mo is not None

    @staticmethod
    def validate_user_fullname(user):
        # Length validation
        # if len(user.full_name) > 50:
        #     raise serializers.ValidationError("Full name can be up to 50 characters long")

        pattern = re.compile(
            r"^[a-zA-Zа-яА-ЯёЁґҐєЄіІїЇ]+[a-zA-Z0-9_а-яА-ЯёЁґҐєЄіІїЇ\s'-]*[a-zA-Zа-яА-ЯёЁґҐєЄіІїЇ]+$", re.UNICODE
        )
        if not bool(pattern.match(user.full_name)):
            raise serializers.ValidationError(
                "The full name can consist of characters from the Latin alphabet or "
                "Cyrillic alphabet. Acceptable special characters: space, hyphen, "
                "apostrophe. The text cannot begin or end with special "
                "characters."
            )

    @staticmethod
    def set_data_to_deleted_user(deleted_user):
        deleted_user.email = getattr(settings, "CUSTOM_SETTINGS_DELETED_USER_EMAIL", None)
        deleted_user.full_name = getattr(settings, "CUSTOM_SETTINGS_DELETED_USER_FULL_NAME", None)
        deleted_user.username = getattr(settings, "CUSTOM_SETTINGS_DELETED_USER_USERNAME", None)

        deleted_user.is_active = False
        deleted_user.is_staff = False
        deleted_user.is_superuser = False

        deleted_user.is_deleted_user = True

        return deleted_user

    @staticmethod
    def get_deleted_user():
        deleted_user, _ = User.objects.get_or_create(is_deleted_user=True)
        return deleted_user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=50)
    full_name = models.CharField(
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=50)],
        max_length=50,
        default="Anonim User",
    )

    username = models.CharField(
        validators=[MinLengthValidator(limit_value=2), MaxLengthValidator(limit_value=32)],
        max_length=32,
        default="anonim_user_1",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_deleted_user = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    username_changed = models.BooleanField(default=False)
    last_full_name_change = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def is_verified(self):
        email_query_set = EmailAddress.objects.filter(email=self.email)
        if not email_query_set.exists():
            return False
        return email_query_set.first().verified

    def save(self, *args, **kwargs):
        user_manager = CustomUserManager()

        if self.is_deleted_user:
            user_manager.set_data_to_deleted_user(self)
            return super().save(*args, **kwargs)

        user_manager.validate_user_fullname(self)
        # username_is_valid = user_manager.validate_user_username(self)
        # if not username_is_valid:
        if self.full_name == "Anonim User":
            self.username = user_manager.generate_unique_username(
                self.full_name,
            )

        user_manager.validate_user_username(self)

        if self.full_name != self._original_full_name:
            self.last_full_name_change = timezone.now()

        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_full_name = self.full_name
