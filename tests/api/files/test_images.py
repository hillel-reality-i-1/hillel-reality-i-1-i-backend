from rest_framework.reverse import reverse
from shutil import rmtree

UPLOAD_IMAGE_LINK = reverse('upload_img')
LOGIN_LINK = reverse('rest_login')


def test_upload_image(image_file, api_client, default_user_profile, user_data):
    user_profile = default_user_profile
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })
    token = response.json()['key']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = api_client.post(UPLOAD_IMAGE_LINK, data={"image": image_file})

    assert response.status_code == 201
    assert "id" in response.json()

    rmtree('/'.join(response.json()["image"].split('http://testserver/')[1].split('/')[:-1]))
