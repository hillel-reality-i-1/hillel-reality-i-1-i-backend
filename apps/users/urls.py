from apps.users.views.custom_register_view import CustomRegisterView
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include
from apps.users.views.register_user_profile_ext_view import RegisterProfileExtView
from apps.users.views.register_user_profile_view import RegisterProfileView
from apps.users.views.user_profile_extended_view import UserProfileExtendedListView
from apps.users.views.user_profile_view import UserProfileListView
from apps.users.views.user_view import UserListView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"user_list", UserListView, basename="user_list")
router.register(r"user_profile", UserProfileListView, basename="user_profile")
router.register(r"user_profile_extended", UserProfileExtendedListView, basename="user_profile_extended")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("auth/registration/account-confirm-email/<str:key>/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path("users/", include(router.urls)),
    path("auth/registration_user_profile/", RegisterProfileView.as_view(), name="rest_register_profile"),
    path("auth/registration_user_profile_ext/", RegisterProfileExtView.as_view(), name="rest_register_profile_ext"),
]

# urlpatterns = [
#     path("auth/", include("dj_rest_auth.urls")),
#     path("auth/registration/", CustomRegisterView.as_view(), name="rest_register"),
# path("auth/registration/account-confirm-email/<str:key>/", VerifyEmailView.as_view(), name="account_confirm_email"),
#     path("users/user_list/", UserListView.as_view(), name="user_list"),
#     path("users/user_detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
#     path("users/user_profile/", UserProfileListView.as_view(), name="user_profile"),
# ]
