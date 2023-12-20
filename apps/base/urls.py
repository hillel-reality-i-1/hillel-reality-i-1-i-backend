from django.views.generic import TemplateView
from django.urls import path


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("createUnAccount/<str:key>/", TemplateView.as_view(), name="front_account_confirm_email"),
    path("createNewPasswordForm/<str:user_id>/<str:key>/", TemplateView.as_view(), name="front_reset_password"),
]
