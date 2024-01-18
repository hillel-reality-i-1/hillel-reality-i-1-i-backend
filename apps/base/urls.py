from django.views.generic import TemplateView
from django.urls import path

from apps.base.views import set_language_api

urlpatterns = [
    path("", TemplateView.as_view(), name="front_home"),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("createUnAccount/<str:key>/", TemplateView.as_view(), name="front_account_confirm_email"),
    path("createUnAccount/", TemplateView.as_view(), name="front_create_profile_from_social_account"),
    path("createNewPasswordForm/<str:user_id>/<str:key>/", TemplateView.as_view(), name="front_reset_password"),
    path("deleteAllContent/<str:key>/", TemplateView.as_view(), name="front_account_delete_all_content"),
    path("set-language/<str:language_code>/", set_language_api, name="set_language"),
    path("change_email/<str:uid>/<str:key>", TemplateView.as_view(), name="front_change_email")
]
