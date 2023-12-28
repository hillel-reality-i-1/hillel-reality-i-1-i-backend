from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from cities_light.models import Country
from django.db.models import Count

from apps.content.models.reaction import Reaction
from apps.files.models import Image
from apps.expert.models import Profession

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(validators=[MinLengthValidator(2)], max_length=100)
    country = models.ManyToManyField(Country, related_name="post_countries")
    content = models.CharField(validators=[MinLengthValidator(100)], max_length=10000)
    images = models.ManyToManyField(Image, related_name="post_images", blank=True)
    professional_tags = models.ManyToManyField(Profession, related_name="professional_tags")
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_images(self):
        return self.images.all()

    def get_professional_tags(self):
        return self.professional_tags.all()

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
        return f"Article {self.title} by {self.author}. Created at {self.creation_date}"
