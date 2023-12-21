from django.core.management import BaseCommand
import os
import json

from apps.expert.models import Profession, Service


class Command(BaseCommand):
    def handle(self, *args, **options):
        script_path = os.path.abspath(__file__)

        script_directory = os.path.dirname(script_path)

        json_file_path = os.path.join(script_directory, "professions_and_services.json")
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
