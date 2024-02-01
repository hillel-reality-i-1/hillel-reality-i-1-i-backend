# import re

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from cities_light.models import Country
from django.db.models import Count
from apps.content.models.reaction import Reaction
from apps.expert.models import Category

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(validators=[MinLengthValidator(2)], max_length=100)
    category = models.ManyToManyField(Category, related_name="post_category")
    country = models.ManyToManyField(Country, related_name="post_countries")
    content = models.CharField(validators=[MinLengthValidator(100)], max_length=10000)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_reactions_count(self):
        return self.reactions.values("reaction_type").annotate(count=Count("id"))

    def get_user_reactions(self, user):
        return self.reactions.filter(user=user).values("reaction_type")

    def get_user_reaction(self, user, reaction_type):
        try:
            return self.reactions.get(user=user, reaction_type=reaction_type)
        except Reaction.DoesNotExist:
            return None

    def __str__(self):
        formatted_creation_date = self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        return f"ID: {self.id}  |  Title: {self.title}  |  Author: {self.author}  |  Created: {formatted_creation_date}"

    #
    # Тегирование юзернеймов пользователей
    #
    # def tag_users_in_content(self):
    #     pattern = r"@(\w+)"
    #     content = self.content
    #
    #     matches = re.findall(pattern, content)
    #
    #     for username in matches:
    #         if User.objects.filter(username=username).exists():
    #             user_profile_link = f'<a href="/profile/{username}">@{username}</a>'
    #             content = content.replace(f"@{username}", user_profile_link)
    #
    #     self.content = content
    #
    # def save(self, *args, **kwargs):
    #     self.tag_users_in_content()
    #     super().save(*args, **kwargs)
