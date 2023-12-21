from django.db import models

from apps.users.models import User


class Reaction(models.Model):
    LIKE = "like"
    LOVE = "love"
    TOGETHER = "together"
    HAHA = "haha"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (LOVE, "Love"),
        (TOGETHER, "Together"),
        (HAHA, "Haha"),
        (WOW, "Wow"),
        (SAD, "Sad"),
        (ANGRY, "Angry"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("user", "post", "reaction_type")
