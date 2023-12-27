from .settings import *  # noqa: F401, F403

DEBUG = False
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 0

CELERY_TASK_ALWAYS_EAGER = True

CUSTOM_SETTINGS_ACCOUNT_EMAIL_CELERY_SEND = False
