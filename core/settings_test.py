from .settings import *  # noqa: F401, F403

DEBUG = False
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 0
