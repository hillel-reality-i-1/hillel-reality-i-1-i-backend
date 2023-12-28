from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

from apps.content.models import Post, Contribution

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
    contribution = models.OneToOneField(Contribution, null=True, blank=True, on_delete=models.SET_NULL)
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.author}. Created at {self.creation_date}"

    def get_helpful_count(self):
        return UserCommentVote.objects.filter(comment=self, helpful=True).count()

    def get_not_helpful_count(self):
        return UserCommentVote.objects.filter(comment=self, helpful=False).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.contribute()

    def contribute(self):
        total_positive_votes = self.helpful_count - self.not_helpful_count

        if total_positive_votes >= 10 and self.is_parent and not self.contribution:
            contribution = Contribution.objects.create(post=self.post, author=self.author, text=self.text)
            self.contribution = contribution
            self.save()
        elif total_positive_votes < 10 and self.is_parent and self.contribution:
            self.contribution.delete()
            self.contribution = None
            self.save()

    def update_vote_counts(self):
        self.helpful_count = self.get_helpful_count()
        self.not_helpful_count = self.get_not_helpful_count()
        Comment.objects.filter(pk=self.pk).update(
            helpful_count=self.helpful_count, not_helpful_count=self.not_helpful_count
        )
