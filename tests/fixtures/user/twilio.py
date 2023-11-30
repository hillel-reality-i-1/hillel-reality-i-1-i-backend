import pytest
from cities_light.models import Country, City

from apps.users.models import UserProfile
from rest_framework.test import APIClient


@pytest.fixture
def user_profile(django_user_model):
    user = django_user_model.objects.create_user(
        email="test@example.com",
        password="testpassword",
        first_name="John",
        last_name="Doe",
    )
    country = Country.objects.create(name="TestCountry")
    city = City.objects.create(name="TestCity", country=country)

    return UserProfile.objects.create(
        user=user,
        phone_number="+380968762591",  # номер ВИталик - киевстар
        about_my_self="Test user",
        country=country,
        city=city,
    )


@pytest.fixture
def authenticated_client(user_profile):
    client = APIClient()
    client.force_authenticate(user=user_profile.user)
    return client


@pytest.fixture
def twilio_verification_fixture(user_profile):
    return {
        "user_profile": user_profile,
    }
