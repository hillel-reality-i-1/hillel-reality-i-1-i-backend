from celery import shared_task
from apps.expert.models import Profession
from django.core.management import call_command


@shared_task
def generate_professions_if_table_is_empty():
    if not Profession.objects.exists():
        call_command('generate_prof_and_serv')
