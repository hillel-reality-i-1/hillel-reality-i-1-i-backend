from apps.files.api.views.upload_portfolio_view import UploadPortfolioView

# from django.views.generic import TemplateView

from apps.users.views.change_email_request_view import ChangeEmailRequestView, ChangeEmailConfirmView
from apps.users.views.custom_google_login_view import SocialLoginView
from apps.users.views.check_user_with_email_exist_view import CheckEmailExists
from apps.users.views.custom_password_reset_view import PasswordResetView
from apps.users.views.custom_register_view import CustomRegisterView
from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
)
from django.urls import path, include

from apps.users.views.delete_all_content_confirm_view import DeleteAllContentConfirmView
from apps.users.views.delete_all_content_view import DeleteAllContentView
from apps.users.views.get_user_profile_by_user_id_view import UserProfileByUserIdView
from apps.users.views.password_reset_confirm_view import PasswordResetConfirmView
from apps.users.views.register_user_profile_ext_view import RegisterProfileExtView
from apps.users.views.register_user_profile_view import RegisterProfileView
from apps.files.api.views.upload_image_view import UploadImageView
from apps.users.views.user_delete_view import UserDeleteView
from apps.users.views.user_profile_extended_view import UserProfileExtendedListView
from apps.users.views.user_profile_view import UserProfileListView
from apps.users.views.user_view import UserListView
from apps.users.views.twilio_send_verification_code_view import SendTwilioVerificationCode
from apps.users.views.twilio_check_verification_code_view import CheckTwilioVerificationCode
from apps.users.views.verify_email_view import VerifyEmailView
from apps.users.views.vonage_views import SendVonageVerificationCode, CheckVonageVerificationCode
from rest_framework.routers import DefaultRouter
from allauth.account import views as allauth_views


router = DefaultRouter()
router.register(r"user_list", UserListView, basename="user_list")
router.register(r"user_profile", UserProfileListView, basename="user_profile")
router.register(r"user_profile_extended", UserProfileExtendedListView, basename="user_profile_extended")

urlpatterns = [
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
    path("users/upload_portfolio/", UploadPortfolioView.as_view(), name="upload_portfolio"),
    path(r"users/user_profile_by_user_id/<int:user_id>/", UserProfileByUserIdView.as_view(), name="get_user_profile"),
    path("auth/registration_user_profile/", RegisterProfileView.as_view(), name="registration_user_profile"),
    path("auth/registration_user_profile_ext/", RegisterProfileExtView.as_view(), name="registration_user_profile_ext"),
    path("accounts/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("accounts/confirm-email/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path("auth/password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "auth/password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("users/", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    path("accounts/delete/", UserDeleteView.as_view(), name="account-delete"),
    path("accounts/delete/content/", DeleteAllContentView.as_view(), name="account-content-delete"),
    path(
        "accounts/delete/content/confirm/", DeleteAllContentConfirmView.as_view(), name="account-content-delete-confirm"
    ),
    path("accounts/check-email/", CheckEmailExists.as_view(), name="check_email_exists"),
]

allauth_views_urlpatterns = [
    path("accounts/signup/", allauth_views.signup, name="account_signup"),
    path("accounts/reauthenticate/", allauth_views.reauthenticate, name="account_reauthenticate"),
    path("accounts/password/set/", allauth_views.password_set, name="account_set_password"),
    path("accounts/inactive/", allauth_views.account_inactive, name="account_inactive"),
    # Email
    path("accounts/email/", allauth_views.email, name="account_email"),
    path("allauth_account/", include("allauth.urls")),
    path("social-login/", SocialLoginView.as_view(), name="social_login"),
]

change_email_urlpatterns = [
    path("change-email/request/", ChangeEmailRequestView.as_view(), name="change-email-request"),
    path(
        "change-email/confirm/<str:uidb64>/<str:token>/", ChangeEmailConfirmView.as_view(), name="change-email-confirm"
    ),
]

urlpatterns += allauth_views_urlpatterns
urlpatterns += change_email_urlpatterns
