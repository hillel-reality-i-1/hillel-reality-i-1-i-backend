from rest_framework import serializers
from cities_light.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name"]
