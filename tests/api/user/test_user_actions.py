from django.urls import reverse


REGISTRATION_LINK = reverse("rest_register")


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
