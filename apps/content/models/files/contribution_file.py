from django.db import models
from ..contribution import Contribution
from apps.files.models import File


class ContributionFile(models.Model):
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
