from django.urls import path

from apps.phonenumbers.views import PhoneNumberConfirmView, PhoneNumberVerifyView

urlpatterns = [
    path("auth/send-verification-code/", PhoneNumberVerifyView.as_view(), name="send-verification-code"),
    path("auth/check-verification-code/", PhoneNumberConfirmView.as_view(), name="check-verification-code"),
]
