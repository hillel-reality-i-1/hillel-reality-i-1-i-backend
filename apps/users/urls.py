from django.views.generic import TemplateView

from apps.users.views.custom_register_view import CustomRegisterView
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ResendEmailVerificationView,
)
from django.urls import path, include
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
    path('accounts/resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("accounts/confirm-email/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path(
        'accounts/account-confirm-email/<str:key>/', TemplateView.as_view(),
        name='front_account_confirm_email',
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
    path("allauth_account", include("allauth.urls"))
]

# urlpatterns += allauth_views_urlpatterns
