from pathlib import Path

import dj_database_url
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.payments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

_database_url = config("DATABASE_URL", default=None)

if _database_url:
    DATABASES = {"default": dj_database_url.parse(_database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="stripe_db"),
            "USER": config("POSTGRES_USER", default="postgres"),
            "PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),
            "HOST": config("POSTGRES_HOST", default="localhost"),
            "PORT": config("POSTGRES_PORT", default="5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STRIPE_PUBLIC_KEY_USD = config("STRIPE_PUBLIC_KEY_USD", default="")
STRIPE_SECRET_KEY_USD = config("STRIPE_SECRET_KEY_USD", default="")
STRIPE_PUBLIC_KEY_EUR = config("STRIPE_PUBLIC_KEY_EUR", default="")
STRIPE_SECRET_KEY_EUR = config("STRIPE_SECRET_KEY_EUR", default="")

STRIPE_CURRENCY_KEYS = {
    "usd": {
        "public": STRIPE_PUBLIC_KEY_USD,
        "secret": STRIPE_SECRET_KEY_USD,
    },
    "eur": {
        "public": STRIPE_PUBLIC_KEY_EUR,
        "secret": STRIPE_SECRET_KEY_EUR,
    },
}
