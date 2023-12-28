from cities_light.models import Country
from django.core.management import BaseCommand
import pandas as pd

from apps.location.models import TranslatedCountry


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_excel("apps/location/management/commands/countries-ukr-5.xlsx")
        ukrainian_names = df["ukrainian_names"].tolist()
        english_names = df["country_name"].tolist()
        dct = {e: u for e, u in zip(english_names, ukrainian_names)}

        countries = Country.objects.all().order_by("name")

        for country in countries:
            country.alternate_names = dct.get(country.name)

        Country.objects.bulk_update(countries, ["alternate_names"])

        translated_countries = [TranslatedCountry(country=country) for country in countries]

        TranslatedCountry.objects.bulk_create(translated_countries)
