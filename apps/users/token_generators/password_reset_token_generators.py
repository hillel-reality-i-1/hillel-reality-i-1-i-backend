from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator as _PasswordResetTokenGenerator

from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.http import int_to_base36, base36_to_int


class PasswordResetTokenGenerator(_PasswordResetTokenGenerator):

    def _make_token_with_timestamp(self, user, timestamp, secret):
        # timestamp is number of seconds since 2001-1-1. Converted to base 36,
        # this gives us a 6 digit string until about 2069.
        ts_b36 = int_to_base36(timestamp)
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        # hash_value = f"{user.pk}{user.password}{login_timestamp}{timestamp}{email}"
        hash_value = f"{user.pk}{login_timestamp}{timestamp}{email}"
        print(timestamp)
        print(hash_value)
        hash_string = salted_hmac(
            self.key_salt,
            hash_value,
            secret=secret,
            algorithm=self.algorithm,
        ).hexdigest()[
            ::2
        ]  # Limit to shorten the URL.
        return "%s-%s" % (ts_b36, hash_string)

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return {'status': False, 'details': 'token is empty'}
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return {'status': False, 'details': 'bad token'}

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return {'status': False, 'details': 'bad token'}

        # Check that the timestamp/uid has not been tampered with
        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return {'status': False, 'details': 'bad token'}

        # Check the timestamp is within limit.
        change_email_timeout = getattr(settings, 'PASSWORD_RESET_TIMEOUT', 900)
        if (self._num_seconds(self._now()) - ts) > change_email_timeout:
            return {'status': False, 'details': 'token expired'}

        return {'status': True, 'details': 'OK'}
