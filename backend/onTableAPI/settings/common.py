import os

SITE_ID = 2

# ------------------------------------------------------------------------------
# Main settings 
# ------------------------------------------------------------------------------

DEBUG = int(os.environ.get("DEBUG", default=1))

SECRET_KEY = os.environ.get("SECRET_KEY","REDACTED_SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS","127.0.0.1").split(" ")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ------------------------------------------------------------------------------
# DATABASE 
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.contrib.gis.db.backends.postgis"), # django.db.backends.postgresql for postgres only
        "NAME": os.environ.get("SQL_DATABASE", "onTable"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "0.0.0.0"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# ------------------------------------------------------------------------------
#ADMINS
# ------------------------------------------------------------------------------
ADMINS = (
    ('Dubanchet Alexis', 'alexisdubanchet@yahoo.com'),
    ('Mont Henry', 'henry.mont@hotmail.fr'),
    ('Carteron Martin', 'carteronmartin@gmail.com'),
)

# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    #'apps.SuitConfig'
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.gis',

    'crispy_forms',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    # Rest_auth
    'rest_auth',
    'rest_auth.registration',

    'django_filters',
    'django.contrib.admindocs',#Documentation

    'core',
    'company',
    'company_manager',


    'django_extensions', #Testing 
]
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #Languages
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'onTableAPI.urls'

# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                "django.template.context_processors.i18n",

                # Custom Context processors 
                'company_manager.context_processors.display_company_name',
                'company_manager.context_processors.display_for_susbcribers1',
                'company_manager.context_processors.frontend_address'
            ],
        },
    },
]

# ------------------------------------------------------------------------------

WSGI_APPLICATION = 'onTableAPI.wsgi.application'

# ------------------------------------------------------------------------------
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')] # <--- delete this ? 
# ------------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'fr-FR'
LANGUAGES = [
    ('fr-FR', 'Français'),
    ('en', 'English'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# MEDIA FILES
#MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_ROOT = '/vol/media'
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# ------------------------------------------------------------------------------
# CUSTOM USER MODEL CONFIGS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'core.CustomUser'

# ------------------------------------------------------------------------------
# DJANGO-ALLAUTH CONFIGS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id

# https://django-allauth.readthedocs.io/en/latest/installation.html?highlight=backends
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE  = True
#ACCOUNT_FORMS = {'signup': 'users.forms.UserSignupForm',}


# ------------------------------------------------------------------------------
# MANAGING MESSAGES (ALERTS,. . .)
# ------------------------------------------------------------------------------
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ------------------------------------------------------------------------------
# Size for uploads
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# ------------------------------------------------------------------------------
MAX_UPLOAD_SIZE = 10485760
MAX_DOCUMENTS_PER_ACCOUNT = 8

# ------------------------------------------------------------------------------
# REST Framework conf
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication', 
    ]
}

# ------------------------------------------------------------------------------
# Celery settings
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL",'redis://redis:6379')
CELERY_NAME = os.environ.get("CELERY_NAME",'onTableAPI')
CELERY_BACKEND = os.environ.get("CELERY_BACKEND",'redis://redis:6379')

CELERY_ACCEPT_CONTENT = os.environ.get("CELERY_ACCEPT_CONTENT",['application/json'])
CELERY_RESULT_SERIALIZER = os.environ.get("CELERY_RESULT_SERIALIZER",'json')
CELERY_TASK_SERIALIZER = os.environ.get("CELERY_TASK_SERIALIZER",'json')

# ------------------------------------------------------------------------------
# FACEBOOK API settings
# ------------------------------------------------------------------------------

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'
        }
    }

# ------------------------------------------------------------------------------
# Configuration of server Mail
# ------------------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND","django.core.mail.backends.filebased.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST",'smtp.gmail.com')
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER",'mail.gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD",'PASSWORD')
EMAIL_PORT = int(os.environ.get("EMAIL_PORT",default=587))
EMAIL_USE_TLS = bool(os.environ.get("EMAIL_USE_TLS"))

if DEBUG:
    EMAIL_FILE_PATH = '/home/app/web/mails'

# ------------------------------------------------------------------------------
# Captcha by Google
# ------------------------------------------------------------------------------
#https://www.google.com/recaptcha/admin/site/352438463/settings
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY","foo")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY","foo")

RECAPTCHA_USE_SSL = True     # Defaults to False

# ------------------------------------------------------------------------------
#Contact us
# ------------------------------------------------------------------------------
SERVER_EMAIL = os.environ.get("SERVER_EMAIL","test@protonmail.com")

# ------------------------------------------------------------------------------
# FRONTEND 
# ------------------------------------------------------------------------------
FRONTEND_ADDRESS = os.environ.get("FRONTEND_ADDRESS","http://localhost:8080/")
