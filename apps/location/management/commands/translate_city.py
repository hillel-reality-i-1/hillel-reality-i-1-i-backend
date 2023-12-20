from cities_light.models import City
from django.core.management import BaseCommand
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_excel("apps/location/management/commands/cities-ukr.xlsx")
        ukrainian_names = tuple(df["name"].tolist())
        cities = City.objects.all().order_by("id")

        for city, ukr_name in zip(cities, ukrainian_names):
            city.alternate_names = ukr_name

        City.objects.bulk_update(cities, ["alternate_names"])