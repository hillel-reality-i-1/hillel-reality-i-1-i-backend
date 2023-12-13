from django.views.generic import TemplateView
from django.urls import path


urlpatterns = [
    path("createUnAccount/<str:key>/", TemplateView.as_view(), name="front_account_confirm_email"),
    path("createNewPasswordForm/<int:user_id>/<str:key>/", TemplateView.as_view(), name="front_reset_password"),
]
