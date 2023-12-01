from rest_framework.reverse import reverse
from shutil import rmtree
from PIL import Image as PilImg

UPLOAD_IMAGE_LINK = reverse("upload_img")
LOGIN_LINK = reverse("rest_login")


def login_user(api_client, user_data):
    response = api_client.post(
        LOGIN_LINK,
        {
            "password": user_data["password"],
            "email": user_data["email"],
        },
    )
    token = response.json()["key"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")


def test_upload_image(simple_image_file, api_client, default_user_profile, user_data):
    login_user(api_client, user_data)
    response = api_client.post(UPLOAD_IMAGE_LINK, data={"image": simple_image_file})

    assert response.status_code == 201
    assert "id" in response.json()

    rmtree("/".join(response.json()["image"].split("http://testserver/")[1].split("/")[:-1]))


def test_image_size_compression(compress_image_file, api_client, default_user_profile, user_data):
    login_user(api_client, user_data)
    response = api_client.post(UPLOAD_IMAGE_LINK, data={"image": compress_image_file})
    path = f'{"/".join(response.json()["image"].split("http://testserver/")[1].split("/")[:-1])}/file.png'

    origin_image = PilImg.open(compress_image_file)
    compressed_image = PilImg.open(path)

    max_size = (320, 240)

    assert origin_image.size[0] > max_size[0]
    assert origin_image.size[1] > max_size[1]

    assert compressed_image.size[0] <= max_size[0]
    assert compressed_image.size[1] <= max_size[1]

    rmtree("/".join(response.json()["image"].split("http://testserver/")[1].split("/")[:-1]))


def test_image_memory_size(big_image_file, api_client, default_user_profile, user_data):
    login_user(api_client, user_data)
    response = api_client.post(UPLOAD_IMAGE_LINK, data={"image": big_image_file})

    assert "Image size exceeds the maximum allowed size (5 MB)." in response.json()


def test_image_format(wrong_ext_image_file, api_client, default_user_profile, user_data):
    login_user(api_client, user_data)
    response = api_client.post(UPLOAD_IMAGE_LINK, data={"image": wrong_ext_image_file})

    assert "Invalid image format. Supported formats: JPEG, PNG." in response.json()
