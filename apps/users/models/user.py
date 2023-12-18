from random import randint
import re

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
        first_name = extra_fields.get("first_name", "")
        last_name = extra_fields.get("last_name", "")
        username = self.generate_unique_username(first_name, last_name)
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    @staticmethod
    def is_username_unique(username):
        return not get_user_model().objects.filter(username=username).exists()

    def generate_unique_username(self, first_name, last_name):
        last_name = last_name if last_name else ""

        username = f"{first_name.lower()}_{last_name.lower()}_{randint(1, 99999)}"

        if not User.objects.count():
            return f"{first_name.lower()}_{last_name.lower()}_{randint(1, 99999)}"

        while not self.is_username_unique(username):
            username = f"{first_name.lower()}_{last_name.lower()}_{randint(1, 99999)}"

        return username

    @staticmethod
    def validate_user_username(user):
        if user.username is None:
            return False

        pattern = rf'\A({user.first_name.lower()}_{user.last_name.lower() if user.last_name else ""}_\d{{1,5}})\Z'
        mo = re.compile(pattern).match(user.username.lower())
        return mo is not None

    @staticmethod
    def set_data_to_deleted_user(deleted_user):
        deleted_user.email = getattr(settings, "CUSTOM_SETTINGS_DELETED_USER_EMAIL", None)
        deleted_user.first_name = getattr(settings, "CUSTOM_SETTINGS_DELETED_USER_FIRST_NAME", None)
        deleted_user.last_name = getattr(settings, "CUSTOM_SETTINGS_DELETED_USER_LAST_NAME", None)
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
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=True)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_deleted_user = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

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

        username_is_valid = user_manager.validate_user_username(self)

        if not username_is_valid:
            if self.first_name == "Anonim_0" and self.last_name == "User_1":
                self.username = user_manager.generate_unique_username(
                    self.first_name,
                    self.last_name,
                )
        return super().save(*args, **kwargs)
