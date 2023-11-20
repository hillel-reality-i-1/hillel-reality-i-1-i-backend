import pytest
from rest_framework.test import APIClient
from .fixtures import *  # noqa: F401, F403


@pytest.fixture(autouse=True, scope='function')
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()
