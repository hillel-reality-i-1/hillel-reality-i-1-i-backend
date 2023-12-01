from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView
from django.views.generic import TemplateView

from apps.users.views.city_view import CityListView
from apps.users.views.country_view import CountryListView
from apps.users.views.custom_register_view import CustomRegisterView
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ResendEmailVerificationView,
)
from django.urls import path, include
from apps.users.views.register_user_profile_ext_view import RegisterProfileExtView
from apps.users.views.register_user_profile_view import RegisterProfileView
from apps.users.views.upload_image_view import UploadImageView
from apps.users.views.user_profile_extended_view import UserProfileExtendedListView
from apps.users.views.user_profile_view import UserProfileListView
from apps.users.views.user_view import UserListView
from apps.users.views.twilio_views import SendTwilioVerificationCode, CheckTwilioVerificationCode
from apps.users.views.vonage_views import SendVonageVerificationCode, CheckVonageVerificationCode
from rest_framework.routers import DefaultRouter
from allauth.account import views as allauth_views


router = DefaultRouter()
router.register(r"user_list", UserListView, basename="user_list")
router.register(r"user_profile", UserProfileListView, basename="user_profile")
router.register(r"user_profile_extended", UserProfileExtendedListView, basename="user_profile_extended")
router.register(r"country_list", CountryListView, basename="country_list")
router.register(r"city_list", CityListView, basename="city_list")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/send-verification-code/", SendTwilioVerificationCode.as_view(), name="send-verification-code"),
    path(
        "auth/send-verification-code-vonage/",
        SendVonageVerificationCode.as_view(),
        name="send-verification-code-vonage",
    ),
    path("auth/check-verification-code/", CheckTwilioVerificationCode.as_view(), name="check-verification-code"),
    path(
        "auth/check-verification-code-vonage/",
        CheckVonageVerificationCode.as_view(),
        name="check-verification-code-vonage",
    ),
    path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("users/upload_img/", UploadImageView.as_view(), name="upload_img"),
    path("auth/registration_user_profile/", RegisterProfileView.as_view(), name="registration_user_profile"),
    path("auth/registration_user_profile_ext/", RegisterProfileExtView.as_view(), name="registration_user_profile_ext"),
    path("accounts/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("accounts/confirm-email/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path(
        "accounts/account-confirm-email/<str:key>/",
        TemplateView.as_view(),
        name="front_account_confirm_email",
    ),
    path("auth/password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("users/", include(router.urls)),
]

allauth_views_urlpatterns = [
    path("accounts/signup/", allauth_views.signup, name="account_signup"),
    path("accounts/reauthenticate/", allauth_views.reauthenticate, name="account_reauthenticate"),
    path("accounts/password/set/", allauth_views.password_set, name="account_set_password"),
    path("accounts/inactive/", allauth_views.account_inactive, name="account_inactive"),
    # Email
    path("accounts/email/", allauth_views.email, name="account_email"),
    path("allauth_account/", include("allauth.urls")),
]

urlpatterns += allauth_views_urlpatterns
