from django.db import models
from django.contrib.auth import get_user_model
from ..contribution import Contribution

User = get_user_model()


class ContributionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
