from django.urls import path

from apps.location.views.cities_by_country_view import CitiesAPIView
from apps.location.views.city_view import CityListView
from apps.location.views.country_view import CountryListView


urlpatterns = [
    path("country_list/", CountryListView.as_view({"get": "list"}), name="country_list"),
    path("city_list/", CityListView.as_view({"get": "list"}), name="city_list"),
    path("cities/", CitiesAPIView.as_view(), name="cities")
]
