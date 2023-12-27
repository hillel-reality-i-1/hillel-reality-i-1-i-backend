from django.views.generic import TemplateView
from django.urls import path

from apps.base.views import set_language_api

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("createUnAccount/<str:key>/", TemplateView.as_view(), name="front_account_confirm_email"),
    path("createNewPasswordForm/<str:user_id>/<str:key>/", TemplateView.as_view(), name="front_reset_password"),
    path("set-language/<str:language_code>/", set_language_api, name="set_language"),
]
