from django.contrib.auth.tokens import PasswordResetTokenGenerator as _PasswordResetTokenGenerator

from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36


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
        hash_value = f"{user.pk}{user.password}{login_timestamp}{timestamp}{email}"
        hash_string = salted_hmac(
            self.key_salt,
            hash_value,
            secret=secret,
            algorithm=self.algorithm,
        ).hexdigest()[
            ::2
        ]  # Limit to shorten the URL.
        return "%s-%s" % (ts_b36, hash_string)
