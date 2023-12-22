from cities_light.models import City
from django.core.management import BaseCommand
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_excel("apps/location/management/commands/cities-5-ukr.xlsx")
        ukrainian_names = df["translated"].tolist()
        english_names = df["origin"].tolist()
        dct = {e: u for e, u in zip(english_names, ukrainian_names)}

        cities = City.objects.all().order_by("name")

        for city in cities:
            city.alternate_names = dct.get(city.name)

        City.objects.bulk_update(cities, ["alternate_names"])
