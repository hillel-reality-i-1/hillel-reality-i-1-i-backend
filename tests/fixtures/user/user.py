import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


def _user_data():
    return {
        'email': 'test@example.com',
        'username': 'test@example.com',
        'password': 'StrongPassword123',
    }


def _create_user(email, username, password):
    return User.objects.create_user(username=username, email=email, password=password)


def get_default_user():
    user = _create_user(**_user_data())
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
