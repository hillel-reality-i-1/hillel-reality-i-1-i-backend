from apps.users.views.custom_register_view import CustomRegisterView
from allauth.account.views import ConfirmEmailView
from django.urls import (
    path,
    include,
)


urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("accounts/confirm-email/<str:key>/", ConfirmEmailView.as_view(), name="account_confirm_email"),
]
