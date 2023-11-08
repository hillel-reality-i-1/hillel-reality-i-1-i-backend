from django.db import models
from ..contribution import Contribution
from apps.files.models import Image


class ContributionImage(models.Model):
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
