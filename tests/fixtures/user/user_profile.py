import pytest
from cities_light.models import Country
from apps.users.models import UserProfile
from . import get_default_verified_user


def _user_profile_data():
    country = Country.objects.create(name='Zurumbia', continent='AF')
    return {
        "country": country,
    }


def _create_user_profile(**data):
    return UserProfile.objects.create(**data)


def get_default_user_profile():
    user = get_default_verified_user()
    user_profile = _create_user_profile(user=user, **_user_profile_data())
    return user_profile


@pytest.fixture()
def user_profile_model():
    return UserProfile


@pytest.fixture()
def user_profile_data():
    return _user_profile_data()


@pytest.fixture()
def default_user_profile():
    return get_default_user_profile()


@pytest.fixture()
def create_user_profile():
    return _create_user_profile
