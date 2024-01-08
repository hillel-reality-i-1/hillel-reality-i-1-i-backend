from django.core.management import BaseCommand
import os
import json

from apps.expert.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        script_path = os.path.abspath(__file__)

        script_directory = os.path.dirname(script_path)

        json_file_path = os.path.join(script_directory, "categories.json")
        with open(json_file_path, encoding="utf-8") as file:
            data = json.load(file)

        for category in data:
            Category.objects.get_or_create(name=category)
