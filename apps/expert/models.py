from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
