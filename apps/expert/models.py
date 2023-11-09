from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="title")
    approved = models.BooleanField(default=False, verbose_name="approved")

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="title")
    approved = models.BooleanField(default=False, verbose_name="approved")

    def __str__(self):
        return self.name
