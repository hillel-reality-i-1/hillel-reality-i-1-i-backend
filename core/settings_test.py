from .settings import *  # noqa: F401, F403

DEBUG = False
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 0

CELERY_TASK_ALWAYS_EAGER = True

CUSTOM_SETTINGS_ACCOUNT_EMAIL_CELERY_SEND = False

POSTGRES_TEST_USER = env.str("POSTGRES_TEST_USER", "test_user")
POSTGRES_TEST_PASSWORD = env.str("POSTGRES_TEST_PASSWORD", "test_password")

DATABASES = {
    "default": env.db_url_config(
        f'postgres://{POSTGRES_TEST_USER}:{POSTGRES_TEST_PASSWORD}'
        f'@{env.str("POSTGRES_HOST")}:{env.str("POSTGRES_PORT")}/test_{env.str("POSTGRES_DB")}',
    )
}
