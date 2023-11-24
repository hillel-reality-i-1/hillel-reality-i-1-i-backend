import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(f"The password must be no more than {self.max_length} characters long.")

        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code="password_no_lowercase",
            )

        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code="password_no_uppercase",
            )

        special_characters = r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]"
        if not re.search(special_characters, password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code="password_no_special_character",
            )

    def get_help_text(self):
        return f"The password must be no more than {self.max_length} characters long."
