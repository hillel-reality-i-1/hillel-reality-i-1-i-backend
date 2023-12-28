from cities_light.models import Country, City
from django.db import models
from django.utils.translation import get_language


class TranslatedCountry(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name="translated_country")

    def translated_name(self, language=None):
        if not language:
            language = get_language()
        if language != "en":
            return self.country.alternate_names
        else:
            return self.country.name

    def __str__(self):
        return self.translated_name()


class TranslatedCity(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name="translated_city")

    def translated_name(self, language=None):
        if not language:
            language = get_language()

        if language != "en":
            return self.city.alternate_names
        else:
            return self.city.name

    def __str__(self):
        return self.translated_name()
