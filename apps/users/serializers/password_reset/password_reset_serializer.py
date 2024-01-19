from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.sites.shortcuts import get_current_site

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import (
    user_username,
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.base.utils import get_frontend_url
from apps.users.token_generators import PasswordResetTokenGenerator


class CustomResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']

        for user in self.users:

            temp_key = PasswordResetTokenGenerator().make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            # url_generator = kwargs.get('url_generator', default_url_generator)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            url = get_frontend_url('front_reset_password', uid, temp_key)

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            if (
                allauth_account_settings.AUTHENTICATION_METHOD
                != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomResetForm
