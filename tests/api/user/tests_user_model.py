import re

from django.urls import reverse
from django.core import mail

REGISTER_LINK = reverse('rest_register')
LOGIN_LINK = reverse('rest_login')
LOGOUT_LINK = reverse('rest_logout')
CONFIRM_EMAIL_LINK = reverse('account_confirm_email')
POST_LIST_LINK = reverse('api-content:posts-list')


def test_create_user(user_data, create_user, user_model):
    create_user(**user_data)
    assert user_model.objects.all().count() == 1


def test_registration_user(user_data, api_client):
    user_data.update(
        {
            "password1": user_data["password"],
            "password2": user_data["password"],
        }
    )
    response = api_client.post(path=REGISTER_LINK, data=user_data)
    assert response.status_code == 201


def test_success_login_user(user_data, create_user, api_client, email_model):
    user = create_user(**user_data)
    email_model.objects.create(user=user, email=user.email, verified=True, primary=True)
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })
    assert response.status_code == 200
    assert 'key' in response.json()


def test_login_user_invalid_password(user_data, create_user, api_client, email_model):
    user = create_user(**user_data)
    email_model.objects.create(user=user, email=user.email, verified=True, primary=True)
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'] + '0',
        'email': user_data['email'],
    })
    assert response.status_code == 400
    assert response.json() == {'non_field_errors': ['Unable to log in with provided credentials.']}


def test_login_user_invalid_email(user_data, create_user, api_client, email_model):
    user = create_user(**user_data)
    email_model.objects.create(user=user, email=user.email, verified=True, primary=True)
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'] + '0',
    })
    assert response.status_code == 400
    assert response.json() == {'non_field_errors': ['Unable to log in with provided credentials.']}


def test_login_user_unverified_email(user_data, create_user, api_client, email_model):
    user = create_user(**user_data)
    email_model.objects.create(user=user, email=user.email, verified=False, primary=True)
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })
    assert response.status_code == 400
    assert response.json() == {'non_field_errors': ['E-mail is not verified.']}


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


def test_verification_email(user_data, api_client):
    user_data.update(
        {
            "password1": user_data["password"],
            "password2": user_data["password"],
        }
    )
    api_client.post(path=REGISTER_LINK, data=user_data)
    assert len(mail.outbox) == 1

    body = mail.outbox[0].body
    key = re.compile(
        pattern=r'.*http.*/([^/]*)/\s'
    ).findall(body)[0]
    data = {"key": key}
    response = api_client.post(CONFIRM_EMAIL_LINK, data=data)
    assert response.status_code == 200

    token = response.json()['token']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = api_client.get(POST_LIST_LINK)

    assert response.status_code == 200
