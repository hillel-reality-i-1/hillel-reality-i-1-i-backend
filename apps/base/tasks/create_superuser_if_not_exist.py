from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.management import call_command


@shared_task
def create_superuser_if_not_exists():
    if not get_user_model().objects.exists():
        call_command('createsuperuser')
