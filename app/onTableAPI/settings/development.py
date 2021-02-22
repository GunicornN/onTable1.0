## onTable/development.py

"""
Settings for the dev

"""
from onTableAPI.settings.common import *
from onTableAPI.settings.celery import *


DEBUG = int(os.environ.get("DEBUG", default=0))

# ------------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'REDACTED_SECRET_KEY' #regenerate secret key 

SECRET_KEY = os.environ.get("SECRET_KEY","REDACTED_SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS","127.0.0.1").split(" ")

# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.contrib.gis.db.backends.postgis"), # django.db.backends.postgresql for postgres only
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "onTable")),
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
# Emails Settings
# More infos at :
#   https://byteschool.io/post/sending-email-with-smtp-on-aws-and-django/
# ------------------------------------------------------------------------------

#feedback-smtp.eu-west-1.amazonses.com
# ------------------------------------------------------------------------------
# Captcha by Google
# ------------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = 'REDACTED_RECAPTCHA_PUBLIC'
RECAPTCHA_PRIVATE_KEY = 'REDACTED_RECAPTCHA_PRIVATE'

RECAPTCHA_USE_SSL = True     # Defaults to False
# ------------------------------------------------------------------------------
#Contact us
# ------------------------------------------------------------------------------
SERVER_EMAIL = 'contact@example.com'

# ------------------------------------------------------------------------------
# Google MAP API keys
# ------------------------------------------------------------------------------
GOOGLE_MAP_API_KEY = 'REDACTED_GOOGLE_MAPS_KEY'

# ------------------------------------------------------------------------------
# FACEBOOK API keys
# ------------------------------------------------------------------------------
SOCIAL_AUTH_FACEBOOK_KEY = 'REDACTED_FACEBOOK_APP_ID'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET ='REDACTED_FACEBOOK_SECRET' #app key