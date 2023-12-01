from celery import shared_task
from cities_light.models import City
from django.core.management import call_command


@shared_task
def populate_cities_if_table_is_empty():
    if not City.objects.exists():
        call_command('cities_light')
