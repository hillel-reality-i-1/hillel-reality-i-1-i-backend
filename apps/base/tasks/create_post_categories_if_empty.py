from celery import shared_task
from django.core.management import call_command
from apps.expert.models import Category


@shared_task
def create_post_categories_if_empty():
    if not Category.objects.exists():
        call_command('create_categories')
