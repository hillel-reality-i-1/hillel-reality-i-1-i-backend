import pytest
from allauth.account.models import EmailAddress


def add_verified_email(user):
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)


def add_unverified_email(user):
    EmailAddress.objects.create(user=user, email=user.email, verified=False, primary=True)


@pytest.fixture
def email_model():
    return EmailAddress
