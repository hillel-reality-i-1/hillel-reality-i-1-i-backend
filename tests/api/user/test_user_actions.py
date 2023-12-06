from django.urls import reverse

from apps.users.models import User

REGISTRATION_LINK = reverse("rest_register")
LOGIN_LINK = reverse("rest_login")
USER_LIST = "/api/v1/users/user_list/"


def login_user(api_client, email, password):
    response = api_client.post(
        LOGIN_LINK,
        {
            "password": password,
            "email": email,
        },
    )
    return response


def test_user_registration_default(api_client, user_data):
    response = api_client.post(
        REGISTRATION_LINK,
        {
            "password1": user_data["password"],
            "password2": user_data["password"],
            "email": user_data["email"],
        },
    )
    email = response.json()["email"]

    assert response.status_code == 201
    assert email == user_data["email"]

    user = User.objects.get(email=email)
    assert "anonim_user" in user.username


def test_login_by_email_password(api_client, user_data, default_verified_user):
    response = login_user(api_client, user_data["email"], user_data["password"])

    assert response.status_code == 200
    assert "key" in response.json()


def test_update_user_first_and_last_name(api_client, user_data, default_verified_user):
    user = User.objects.get(email=user_data["email"])

    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]

    response = login_user(api_client, user_data["email"], user_data["password"])
    token = response.json()["key"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response_login = api_client.patch(
        f"{USER_LIST}{user.pk}/", data={"first_name": "test_first", "last_name": "test_last"}
    )

    assert response_login.status_code == 200

    user = User.objects.get(email=user_data["email"])
    assert user.first_name == "test_first"
    assert user.last_name == "test_last"


def test_create_user_profile():
    pass
