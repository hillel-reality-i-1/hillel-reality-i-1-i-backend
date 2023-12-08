from cities_light.models import Country, City
from django.urls import reverse

from apps.users.models import User

REGISTRATION_LINK = reverse("rest_register")
REG_USER_PROFILE = reverse("registration_user_profile")
LOGIN_LINK = reverse("rest_login")
USER_LIST = "/api/v1/users/user_list/"
PROFILE_LIST = "/api/v1/users/user_profile/"


def login_user(api_client, email, password):
    response = api_client.post(
        LOGIN_LINK,
        {
            "password": password,
            "email": email,
        },
    )
    return response


def put_credentials_into_apiclient(api_client, user_data):
    response = login_user(api_client, user_data["email"], user_data["password"])
    token = response.json()["key"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")


def profile_data():
    country = Country.objects.create(name="Zurumbia", continent="AF")
    city = City.objects.create(country_id=country.id, name="Odessa")
    profile_user_data = {
        "phone_number": "+380979998877",
        "about_my_self": "About my Self",
        "country_id": country.id,
        "city_id": city.id,
    }

    return profile_user_data


class TestUserActions:
    def test_user_registration_default(self, api_client, user_data):
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

    def test_error_user_registration(self, api_client, user_data, default_verified_user):
        response = api_client.post(
            REGISTRATION_LINK,
            {
                "password1": user_data["password"],
                "password2": user_data["password"],
                "email": user_data["email"],
            },
        )

        assert "This email is already in use. Please, use another or sign in" in response.json()["email"]

    def test_login_by_email_password(self, api_client, user_data, default_verified_user):
        response = login_user(api_client, user_data["email"], user_data["password"])

        assert response.status_code == 200
        assert "key" in response.json()

    def test_update_user_first_and_last_name(self, api_client, user_data, default_verified_user):
        user = User.objects.get(email=user_data["email"])

        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]

        put_credentials_into_apiclient(api_client, user_data)
        response_login = api_client.patch(
            f"{USER_LIST}{user.pk}/", data={"first_name": "test_first", "last_name": "test_last"}
        )

        assert response_login.status_code == 200

        user = User.objects.get(email=user_data["email"])
        assert user.first_name == "test_first"
        assert user.last_name == "test_last"

    def test_create_user_profile(self, api_client, user_data, default_verified_user):
        profile_user_data = profile_data()
        print(profile_user_data)
        put_credentials_into_apiclient(api_client, user_data)
        response_login = api_client.post(REG_USER_PROFILE, data=profile_user_data)

        db_data = response_login.json()
        print(db_data)
        assert response_login.status_code == 201
        assert db_data["phone_number"] == profile_user_data["phone_number"]
        assert db_data["about_my_self"] == profile_user_data["about_my_self"]
        assert db_data["country"]["id"] == profile_user_data["country_id"]
        assert db_data["city"]["id"] == profile_user_data["city_id"]

    def test_error_create_user_profile(self, api_client, user_data, default_user_profile):
        profile_user_data = profile_data()
        put_credentials_into_apiclient(api_client, user_data)
        response_login = api_client.post(REG_USER_PROFILE, data=profile_user_data)

        assert "This user already has a profile" in response_login.json()

    def test_update_user_profile_data(self, api_client, user_data, default_user_profile):
        user = User.objects.get(email=user_data["email"])
        profile_user_data = profile_data()
        put_credentials_into_apiclient(api_client, user_data)
        response_login = api_client.patch(f"{PROFILE_LIST}{user.userprofile.pk}/", data=profile_user_data)
        print(response_login.json())
        assert response_login.status_code == 200

        user = User.objects.get(email=user_data["email"])
        assert user.userprofile.phone_number == profile_user_data["phone_number"]
        assert user.userprofile.about_my_self == profile_user_data["about_my_self"]
        assert user.userprofile.country.id == profile_user_data["country_id"]
        assert user.userprofile.city.id == profile_user_data["city_id"]
