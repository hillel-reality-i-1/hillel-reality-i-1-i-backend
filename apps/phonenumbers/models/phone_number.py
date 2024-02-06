import hashlib

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class PhoneNumber(models.Model):
    number = models.CharField(max_length=20)
    verification_code_hashed = models.CharField(max_length=128, blank=True)
    verified = models.BooleanField(default=False)
    verification_code_timestamp = models.DateTimeField(blank=True, null=True)

    def generate_verification_code(self):
        code = get_random_string(length=4, allowed_chars='0123456789')
        self.verification_code_hashed = self.hash_function(code)
        self.verification_code_timestamp = timezone.now()
        self.save()
        return code

    @staticmethod
    def hash_function(code):
        return hashlib.sha256(code.encode()).hexdigest()

    def __str__(self):
        return self.number
