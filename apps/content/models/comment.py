from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from .post import Post

User = get_user_model()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(validators=[MinLengthValidator(2), MaxLengthValidator(10000)])
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author}. Created at {self.creation_date}"
