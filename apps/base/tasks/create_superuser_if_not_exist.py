from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.conf import settings


@shared_task
def create_superuser_if_not_exists():
    if not get_user_model().objects.exists():
        full_name = getattr(settings, "DJANGO_SUPERUSER_FULLNAME", "Super User")
        call_command('createsuperuser', f"--full_name={full_name}", "--noinput")
