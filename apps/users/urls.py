from apps.users.views.custom_register_view import CustomRegisterView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from django.urls import path, include
from apps.users.views.register_user_profile_ext_view import RegisterProfileExtView
from apps.users.views.register_user_profile_view import RegisterProfileView
from apps.users.views.user_profile_extended_view import UserProfileExtendedListView
from apps.users.views.user_profile_view import UserProfileListView
from apps.users.views.user_view import UserListView
from apps.users.views.custom_confirm_email_view import CustomConfirmEmailView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"user_list", UserListView, basename="user_list")
router.register(r"user_profile", UserProfileListView, basename="user_profile")
router.register(r"user_profile_extended", UserProfileExtendedListView, basename="user_profile_extended")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("auth/registration_user_profile/", RegisterProfileView.as_view(), name="registration_user_profile"),
    path("auth/registration_user_profile_ext/", RegisterProfileExtView.as_view(), name="registration_user_profile_ext"),
    path("accounts/", include("allauth.urls")),
    path("accounts/confirm-email/", CustomConfirmEmailView.as_view(), name="account_confirm_email"),
    path("accounts/verify-email", VerifyEmailView().as_view(), name="account_email_verification_sent"),
    path("users/", include(router.urls)),
]
