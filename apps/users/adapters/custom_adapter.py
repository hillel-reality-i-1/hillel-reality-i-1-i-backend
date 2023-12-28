from allauth.account.adapter import DefaultAccountAdapter
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

from apps.base.utils import get_frontend_url
from apps.users.tasks import send_adapter_mail_task


class CustomAdapter(DefaultAccountAdapter):

    def send_delete_all_content_confirmation_email(self, user, key):
        delete_all_content_url = self.get_delete_all_content_url(key)
        ctx = {
            "delete_all_content_url": delete_all_content_url,
        }
        email_template = "account/delete_all_content"
        self.send_mail(email_template, user.email, ctx)

    def get_delete_all_content_url(self, key):
        url = get_frontend_url('front_account_delete_all_content', key)
        return url

    def respond_email_verification_sent(self, request, user):
        return Response({"detail": "Verification e-mail sent."}, status=status.HTTP_201_CREATED)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = get_frontend_url('front_account_confirm_email', emailconfirmation.key)
        # url = reverse("front_account_confirm_email", args=[emailconfirmation.key])
        # ret = build_absolute_uri(request, url)
        # print(ret)
        return url

    def send_mail(self, template_prefix, email, context):
        if getattr(settings, 'CUSTOM_SETTINGS_ACCOUNT_EMAIL_CELERY_SEND', False):
            msg = self.render_mail(template_prefix, email, context)
            # Serialize the message
            serialized_msg = msg.__dict__
            send_adapter_mail_task.delay(serialized_msg)
        else:
            super().send_mail(template_prefix, email, context)
