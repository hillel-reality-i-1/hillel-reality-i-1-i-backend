from random import randint

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


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

    def is_username_unique(self, username):
        return not self.get_queryset().filter(username=username).exists()

    def generate_unique_username(self, first_name, last_name):
        username = f"{first_name.lower()}_{last_name.lower()}_{randint(1, 99999)}"

        while not self.is_username_unique(username):
            username = f"{first_name.lower()}_{last_name.lower()}_{randint(1, 99999)}"

        return username


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=150)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
