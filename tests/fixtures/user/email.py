import pytest
from allauth.account.models import EmailAddress


@pytest.fixture
def email_model():
    return EmailAddress
