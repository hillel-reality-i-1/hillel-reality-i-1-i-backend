from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.content.models import Post, Comment
from apps.users.models.user import CustomUserManager


User = get_user_model()


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    def change_author_for_all(old_author, new_author, model):
        query = model.objects.filter(author=old_author)
        for item in query:
            item.author = new_author
            item.save()

    deleted_user = CustomUserManager.get_deleted_user()

    change_author_for_all(instance, deleted_user, Post)
    change_author_for_all(instance, deleted_user, Comment)
