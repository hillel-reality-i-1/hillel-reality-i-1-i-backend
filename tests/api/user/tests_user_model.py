import re

from django.urls import reverse
from django.core import mail

REGISTER_LINK = reverse('rest_register')
LOGIN_LINK = reverse('rest_login')
LOGOUT_LINK = reverse('rest_logout')
CONFIRM_EMAIL_LINK = reverse('account_confirm_email')


def test_create_user(user_data, create_user, user_model):
    create_user(**user_data)
    assert user_model.objects.all().count() == 1


def test_registration_user(user_data, api_client):

    response = api_client.post(path=REGISTER_LINK, data=user_data)

    assert response.status_code == 201


def test_login_user(user_data, create_user, api_client, email_model):

    user = create_user(**user_data)

    email_model.objects.create(user=user, email=user.email, verified=True, primary=True)

    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })

    assert response.status_code == 200
    assert 'key' in response.json()


def test_logout_user(user_data, create_user, api_client, email_model):

    user = create_user(**user_data)

    email_model.objects.create(user=user, email=user.email, verified=True, primary=True)

    api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })

    response = api_client.post(LOGOUT_LINK)

    assert response.status_code == 200
    assert response.json() == {'detail': 'Successfully logged out.'}


def test_verification_by_mail(user_data, api_client):

    api_client.post(path=REGISTER_LINK, data=user_data)

    assert len(mail.outbox) == 1

    body = mail.outbox[0].body

    key = re.compile(
        pattern=r'.*http.*/([^/]*)/\s'
    ).findall(body)[0]

    data = {"key": key}

    response = api_client.post(CONFIRM_EMAIL_LINK, data=data)

    assert response.status_code == 200
    assert response.data == {'detail': 'ok'}

    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })

    assert response.status_code == 200

