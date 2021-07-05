## onTable/development.py

"""
Settings for the dev

"""
from onTableAPI.settings.common import *

DEBUG = int(os.environ.get("DEBUG", default=1))

# ------------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-env")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(" ")

# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.contrib.gis.db.backends.postgis"),
        "NAME": os.environ.get("SQL_DATABASE", "ontable"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "0.0.0.0"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# ------------------------------------------------------------------------------
# Local EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@example.com'

# ------------------------------------------------------------------------------
# Captcha by Google
# ------------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")
RECAPTCHA_USE_SSL = True

# ------------------------------------------------------------------------------
# Contact
# ------------------------------------------------------------------------------
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "contact@example.com")

# ------------------------------------------------------------------------------
# Google MAP API keys
# ------------------------------------------------------------------------------
GOOGLE_MAP_API_KEY = os.environ.get("GOOGLE_MAP_API_KEY", "")

# ------------------------------------------------------------------------------
# FACEBOOK API keys
# ------------------------------------------------------------------------------
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY", "")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET", "")
