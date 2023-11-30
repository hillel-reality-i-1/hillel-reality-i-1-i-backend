from django.core.management import BaseCommand
import os
import json
import django

from apps.expert.models import Profession, Service

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


class Command(BaseCommand):
    def handle(self, *args, **options):
        json_file_path = os.environ.get("JSON_FILE_PATH", "professions_and_services.json")
        with open(json_file_path, encoding="utf-8") as file:
            data = json.load(file)

        """
            Load in db Professions and Services
        """

        for profession_name, services_list in data.items():
            profession, created = Profession.objects.get_or_create(name=profession_name)

            for service_name in services_list:
                service, created = Service.objects.get_or_create(name=service_name)
                service.professions.add(profession)
