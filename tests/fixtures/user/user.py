import pytest
from django.contrib.auth import get_user_model
from .email import add_verified_email, add_unverified_email

User = get_user_model()


def _user_data():
    return {
        'email': 'test@test.test',
        'password': 'StrongPassword123',
        'first_name': 'first_name',
        'last_name': 'last_name',
    }


def _create_user(**user_data):
    return User.objects.create_user(**user_data)


def get_default_user():
    user = _create_user(**_user_data())
    return user


def get_default_verified_user():
    user = get_default_user()
    add_verified_email(user)
    return user


def get_default_unverified_user():
    user = get_default_user()
    add_unverified_email(user)
    return user


@pytest.fixture
def user_data():
    return _user_data()


@pytest.fixture
def create_user():
    return _create_user


@pytest.fixture
def user_model():
    return get_user_model()


@pytest.fixture()
def default_user():
    return get_default_user()


@pytest.fixture()
def default_verified_user():
    return get_default_verified_user()


@pytest.fixture()
def default_unverified_user():
    return get_default_unverified_user()
