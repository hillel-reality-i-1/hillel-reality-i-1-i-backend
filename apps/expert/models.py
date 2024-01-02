from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, verbose_name="name")
    services = models.ManyToManyField("Service", related_name="professions")
    approved = models.BooleanField(default=False, verbose_name="approved")

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, verbose_name="name")
    approved = models.BooleanField(default=False, verbose_name="approved")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, verbose_name="name")
    approved = models.BooleanField(default=False, verbose_name="approved")

    def __str__(self):
        return self.name
