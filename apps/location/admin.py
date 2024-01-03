from django.contrib import admin

from apps.location.models import TranslatedCity, TranslatedCountry

admin.site.register(TranslatedCity)
admin.site.register(TranslatedCountry)
