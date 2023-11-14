from django.urls import reverse

REGISTER_LINK = reverse('rest_register')


def test_create_user(user_data, create_user, user_model):
    create_user(**user_data)
    assert user_model.objects.all().count() == 1


def test_registration_user(user_data, api_client):

    user_data['first_name'] = 'first_name'
    user_data['last_name'] = 'last_name'

    response = api_client.post(path=REGISTER_LINK, data=user_data)

    assert response.status_code == 201
