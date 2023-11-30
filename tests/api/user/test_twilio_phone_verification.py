from django.urls import reverse
from rest_framework import status


def test_send_twilio_verification_code(authenticated_client, twilio_verification_fixture):
    url = reverse("send-verification-code")
    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert "status" in response.data
    assert response.data["status"] == "pending"


def test_check_twilio_verification_code(authenticated_client, twilio_verification_fixture):
    verification_code = "893296"

    check_url = reverse("check-verification-code")
    check_data = {"verification_code": verification_code}
    check_response = authenticated_client.post(check_url, data=check_data)

    assert check_response.status_code == status.HTTP_200_OK
    assert "status" in check_response.data
    assert check_response.data["status"] == "approved"
