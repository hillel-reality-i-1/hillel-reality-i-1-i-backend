from cities_light.models import Country
from django.core.management import BaseCommand
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_excel("apps/location/management/commands/translated_countries.xlsx")
        ukrainian_names = tuple(df["ukrainian_names"].tolist())
        countries = Country.objects.all().order_by("id")

        for country, ukr_name in zip(countries, ukrainian_names):
            country.alternate_names = ukr_name

        Country.objects.bulk_update(countries, ["alternate_names"])
