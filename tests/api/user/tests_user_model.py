import re

from django.urls import reverse
from django.core import mail

REGISTER_LINK = reverse('rest_register')
LOGIN_LINK = reverse('rest_login')
CONFIRM_EMAIL_LINK = reverse('account_confirm_email')


def test_create_user(user_data, create_user, user_model):
    create_user(**user_data)
    assert user_model.objects.all().count() == 1


def test_registration_user(user_data, api_client):

    user_data['first_name'] = 'first_name'
    user_data['last_name'] = 'last_name'

    response = api_client.post(path=REGISTER_LINK, data=user_data)

    assert response.status_code == 201


def test_verification_by_mail(user_data, api_client):

    user_data['first_name'] = 'first_name'
    user_data['last_name'] = 'last_name'

    api_client.post(path=REGISTER_LINK, data=user_data)

    assert len(mail.outbox) == 1

    body = mail.outbox[0].body

    key = re.compile(
        pattern=r'.*http.*/([^/]*)/\s'
    ).findall(body)[0]

    data = {"key": key}

    response = api_client.post(CONFIRM_EMAIL_LINK, data=data)

    print(response.json())

    assert response.status_code == 200
    assert response.data == {'detail': 'ok'}

    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })

    assert response.status_code == 200

