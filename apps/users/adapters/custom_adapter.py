from django.urls import reverse
from allauth.utils import (
    build_absolute_uri,
)
from allauth.account.adapter import DefaultAccountAdapter
from rest_framework import status
from rest_framework.response import Response

from apps.users.tasks import send_adapter_mail_task


class CustomAdapter(DefaultAccountAdapter):

    def respond_email_verification_sent(self, request, user):
        return Response({"detail": "Verification e-mail sent."}, status=status.HTTP_201_CREATED)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse("front_account_confirm_email", args=[emailconfirmation.key])
        ret = build_absolute_uri(request, url)
        return ret

    def send_mail(self, template_prefix, email, context, fail_silently=False):
        msg = self.render_mail(template_prefix, email, context)
        # Serialize the message
        serialized_msg = msg.__dict__
        send_adapter_mail_task.delay(serialized_msg)
