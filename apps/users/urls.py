from apps.users.views.custom_register_view import CustomRegisterView
from apps.users.views.custom_confirm_email_view import CustomConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include, re_path
from apps.users.views.register_user_profile_ext_view import RegisterProfileExtView
from apps.users.views.register_user_profile_view import RegisterProfileView
from apps.users.views.user_profile_extended_view import UserProfileExtendedListView
from apps.users.views.user_profile_view import UserProfileListView
from apps.users.views.user_view import UserListView
from rest_framework.routers import DefaultRouter

from allauth.account import views as allauth_views


router = DefaultRouter()
router.register(r"user_list", UserListView, basename="user_list")
router.register(r"user_profile", UserProfileListView, basename="user_profile")
router.register(r"user_profile_extended", UserProfileExtendedListView, basename="user_profile_extended")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("auth/registration_user_profile/", RegisterProfileView.as_view(), name="registration_user_profile"),
    path("auth/registration_user_profile_ext/", RegisterProfileExtView.as_view(), name="registration_user_profile_ext"),
    path("users/", include(router.urls)),
]

allauth_views_urlpatterns = [
    path("accounts/signup/", allauth_views.signup, name="account_signup"),
    path("accounts/login/", allauth_views.login, name="account_login"),
    path("accounts/logout/", allauth_views.logout, name="account_logout"),
    path("accounts/reauthenticate/", allauth_views.reauthenticate, name="account_reauthenticate"),
    path(
        "accounts/password/change/",
        allauth_views.password_change,
        name="account_change_password",
    ),
    path("accounts/password/set/", allauth_views.password_set, name="account_set_password"),
    path("accounts/inactive/", allauth_views.account_inactive, name="account_inactive"),
    # Email
    path("accounts/email/", allauth_views.email, name="account_email"),
    path("accounts/verify-email/", VerifyEmailView().as_view(), name="account_email_verification_sent"),
    path("accounts/confirm-email/", CustomConfirmEmailView.as_view(), name="account_confirm_email"),
    # password reset
    path("accounts/password/reset/", allauth_views.password_reset, name="account_reset_password"),
    path(
        "accounts/password/reset/done/",
        allauth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "accounts/password/reset/key/done/",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
]

urlpatterns += allauth_views_urlpatterns
