import re

from django.urls import reverse
from django.core import mail

REGISTER_LINK = reverse('rest_register')


def test_create_user(user_data, create_user, user_model):
    create_user(**user_data)
    assert user_model.objects.all().count() == 1


def test_registration_user(user_data, api_client):

    user_data['first_name'] = 'first_name'
    user_data['last_name'] = 'last_name'

    response = api_client.post(path=REGISTER_LINK, data=user_data)

    assert response.status_code == 201


def test_verification_mail_send(user_data, api_client):

    user_data['first_name'] = 'first_name'
    user_data['last_name'] = 'last_name'
    user_data['email'] = 'mizerisaid1722@gmail.com'

    api_client.post(path=REGISTER_LINK, data=user_data)

    assert len(mail.outbox) == 1

    body = mail.outbox[0].body

    url = re.compile(
        pattern=r'.*(http.*)\s'
    ).findall(body)[0]

    print(body)

    response = api_client.get(url)

    print(response)
