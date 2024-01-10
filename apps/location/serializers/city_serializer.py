from django.utils.translation import get_language
from rest_framework import serializers
from cities_light.models import City


class CitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    country = serializers.IntegerField(required=False)

    class Meta:
        model = City
        fields = ["id", "name", "country"]

    def get_name(self, obj):
        language = get_language()
        return obj.alternate_names if language == "uk" else obj.name
