from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

from apps.content.models import Post

User = get_user_model()


class UserCommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    helpful = models.BooleanField()

    class Meta:
        unique_together = ("user", "comment")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(validators=[MinLengthValidator(2), MaxLengthValidator(10000)])
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    is_parent = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_contribution = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)

    def __str__(self):
        formatted_creation_date = self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        return f"ID: {self.id}  |  Comment by {self.author}  |  Created: {formatted_creation_date}"

    def get_helpful_count(self):
        return UserCommentVote.objects.filter(comment=self, helpful=True).count()

    def get_not_helpful_count(self):
        return UserCommentVote.objects.filter(comment=self, helpful=False).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.contribute()

    def contribute(self):
        total_positive_votes = self.helpful_count - self.not_helpful_count

        if total_positive_votes >= 3 and self.is_parent and not self.is_contribution:
            self.is_contribution = True
            self.save()

            user_profile = self.author.userprofile
            user_profile.last_contributions.add(self)
            user_profile.save()

        elif total_positive_votes < 10 and self.is_parent and self.is_contribution:
            self.is_contribution = False
            self.save()

            user_profile = self.author.userprofile
            user_profile.last_contributions.remove(self)
            user_profile.save()

    def update_vote_counts(self):
        self.helpful_count = self.get_helpful_count()
        self.not_helpful_count = self.get_not_helpful_count()
        Comment.objects.filter(pk=self.pk).update(
            helpful_count=self.helpful_count, not_helpful_count=self.not_helpful_count
        )
