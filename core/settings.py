"""
Django's settings for shared__django__example_2023_06_23 project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path

# noinspection PyPackageRequirements
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR.joinpath("apps")

env = environ.FileAwareEnv()
env.read_env(BASE_DIR.joinpath(".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO__SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO__DEBUG", False)

ALLOWED_HOSTS = env.list("DJANGO__ALLOWED_HOSTS", default=[])
if DEBUG:
    ALLOWED_HOSTS.extend(
        [
            "localhost",
            "0.0.0.0",
            "127.0.0.1",
            "51.20.204.164",
            "ec2-51-20-204-164.eu-north-1.compute.amazonaws.com",
        ]
    )

# [applications]-[BEGIN]

# Built-in Django applications.
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

# Local applications.
LOCAL_APPS = [
    # Shared, utils, etc.
    "apps.base",
    # Users and related.
    "apps.users",
    "apps.expert",
    "apps.content",
    "apps.files",
]

# Third-party installed applications.
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    "cities_light",
    "dj_rest_auth.registration",
    # "drf_yasg",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
# [applications]-[END]

SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "core.urls"

AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APPS_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'post.permissions.IsAdminOrReadOnly'
    # ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": env.db_url_config(
        # postgres://user:password@host:port/dbname
        env.str(
            "DJANGO__DB_URL",
            f'postgres://{env.str("POSTGRES_USER")}:{env.str("POSTGRES_PASSWORD")}'
            f'@{env.str("POSTGRES_HOST")}:{env.str("POSTGRES_PORT")}/{env.str("POSTGRES_DB")}',
        )
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "core.password_validation.CustomPasswordValidator",
        "OPTIONS": {
            "max_length": 16,
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Superuser
DJANGO_SUPERUSER_PASSWORD = env.str("DJANGO_SUPERUSER_PASSWORD", "django@pass123")
DJANGO_SUPERUSER_USERNAME = env.str("DJANGO_SUPERUSER_USERNAME", "django_super")
DJANGO_SUPERUSER_EMAIL = env.str("DJANGO_SUPERUSER_EMAIL", "django@gjan.go")
DJANGO_SUPERUSER_FIRST_NAME = env.str("DJANGO_SUPERUSER_FIRST_NAME", "Firstname")
DJANGO_SUPERUSER_LAST_NAME = env.str("DJANGO_SUPERUSER_LAST_NAME", "Lastname")

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "APP": {
            "client_id": env.str("SOCIAL_APP_CLIENT_ID", ""),
            "secret": env.str("SOCIAL_APP_SECRET_KEY", ""),
            "key": "",
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "SOCIALACCOUNT_EMAIL_VERIFICATION": "none",  # Без подтверждения по электронной почте
        "SOCIALACCOUNT_AUTO_SIGNUP": True,
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

CELERY_BROKER_URL = "amqp://{}:{}@{}:{}//".format(
    env.str("RABBITMQ_DEFAULT_USER", "guest"),
    env.str("RABBITMQ_DEFAULT_PASS", "guest"),
    env.str("RABBITMQ_DEFAULT_HOST", "127.0.0.1"),
    env.str("RABBITMQ_DEFAULT_PORT", "5672"),
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

CUSTOM_SETTINGS_ACCOUNT_EMAIL_CELERY_SEND = True
CUSTOM_SETTINGS_DELETED_USER_EMAIL = env.str("CUSTOM_SETTINGS_DELETED_USER_EMAIL", "delet@ed.user")
CUSTOM_SETTINGS_DELETED_USER_FIRST_NAME = env.str("CUSTOM_SETTINGS_DELETED_USER_FIRST_NAME", "Deleted")
CUSTOM_SETTINGS_DELETED_USER_LAST_NAME = env.str("CUSTOM_SETTINGS_DELETED_USER_LAST_NAME", "User")
CUSTOM_SETTINGS_DELETED_USER_USERNAME = env.str("CUSTOM_SETTINGS_DELETED_USER_USERNAME", "deleted_user")

SITE_ID = 1
ACCOUNT_ADAPTER = "apps.users.adapters.CustomAdapter"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

FRONTEND_DOMAIN = env.str("FRONTEND_DOMAIN", None)

REST_AUTH_SERIALIZERS = {
    "PASSWORD_RESET_SERIALIZER": "apps.users.serializers.password_reset_serializer.CustomPasswordResetSerializer",
}

ACCOUNT_EXTRA_REQUIRED_FIELDS = ["first_name"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "email_user")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "email_password")
AUTHENTICATION_CLASSES = [
    "dj_rest_auth.authentication.AllAuthJWTAuthentication",
]

REST_USE_JWT = True
JWT_AUTH_COOKIE = "access_token"

# CORS
CORS_ALLOWED_ORIGINS = [
    # Frond-end origins
    "http://localhost:3000",
]

# API settings for phone_number verification
TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID", "twilio_account")
TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN", "twilio_token")
TWILIO_VERIFY_SID = env.str("TWILIO_VERIFY_SID", "")

VONAGE_API_KEY = env.str("VONAGE_API_KEY", "")
VONAGE_API_SECRET = env.str("VONAGE_API_SECRET", "")
