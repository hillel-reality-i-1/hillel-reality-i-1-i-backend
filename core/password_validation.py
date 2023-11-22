from django.core.exceptions import ValidationError


class MaxLengthValidator:
    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(f"The password must be no more than {self.max_length} characters long.")

    def get_help_text(self):
        return f"The password must be no more than {self.max_length} characters long."
