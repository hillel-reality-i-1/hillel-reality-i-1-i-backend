from apps.users.views.custom_register_view import CustomRegisterView
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include
from apps.users.views.user_view import UserListView


urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("auth/registration/account-confirm-email/<str:key>/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path("users/user_list/", UserListView.as_view(), name="user_list"),
]
