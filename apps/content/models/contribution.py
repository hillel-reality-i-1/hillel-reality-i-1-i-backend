from django.db import models
from django.contrib.auth import get_user_model

from apps.content.models import Post

User = get_user_model()


class ContributionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contribution = models.ForeignKey("Contribution", on_delete=models.CASCADE)
    helpful = models.BooleanField()

    class Meta:
        unique_together = ("user", "contribution")


class Contribution(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.author}. Created at {self.creation_date}"

    def contribute_vote(self, user, helpful):
        existing_vote = ContributionVote.objects.filter(user=user, contribution=self).first()

        if existing_vote:
            if existing_vote.helpful == helpful:
                existing_vote.delete()
            else:
                existing_vote.helpful = helpful
                existing_vote.save()
        else:
            ContributionVote.objects.create(user=user, contribution=self, helpful=helpful)

        self.update_counts()

    def update_counts(self):
        self.helpful_count = ContributionVote.objects.filter(contribution=self, helpful=True).count()
        self.save()
