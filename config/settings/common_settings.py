"""
Base settings to build other settings files upon.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

from dj_database_url import parse as db_url


# We use a 'tuple' with pipes as delimiters as decople naively splits the global
# variables on commas when casting to Csv()
def pipe_delim(pipe_string):
    # Remove opening and closing brackets
    pipe_string = pipe_string[1:-1]
    # Split on pipe delim
    return pipe_string.split("|")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "django_property_filter",
    "modernrpc",
    "mathesar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mathesar.middleware.CursorClosedHandlerMiddleware",
    "mathesar.middleware.PasswordChangeNeededMiddleware",
]

ROOT_URLCONF = "config.urls"

MODERNRPC_METHODS_MODULES = [
    'mathesar.rpc.collaborators',
    'mathesar.rpc.columns',
    'mathesar.rpc.columns.metadata',
    'mathesar.rpc.constraints',
    'mathesar.rpc.data_modeling',
    'mathesar.rpc.databases',
    'mathesar.rpc.databases.configured',
    'mathesar.rpc.databases.privileges',
    'mathesar.rpc.databases.setup',
    'mathesar.rpc.explorations',
    'mathesar.rpc.records',
    'mathesar.rpc.roles',
    'mathesar.rpc.roles.configured',
    'mathesar.rpc.schemas',
    'mathesar.rpc.schemas.privileges',
    'mathesar.rpc.servers.configured',
    'mathesar.rpc.tables',
    'mathesar.rpc.tables.metadata',
    'mathesar.rpc.tables.privileges',
    'mathesar.rpc.users'
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "config.context_processors.frontend_settings",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mathesar.template_context_processors.base_template_extensions.script_extension_templates"
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# TODO: Add to documentation that database keys should not be than 128 characters.

# MATHESAR_DATABASES should be of the form '({db_name}|{db_url}), ({db_name}|{db_url})'
# See pipe_delim above for why we use pipes as delimiters
DATABASES = {
    db_key: db_url(url_string)
    for db_key, url_string in [pipe_delim(i) for i in os.environ.get('MATHESAR_DATABASES', default='').split(',') if i != '']
}

# POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST & POSTGRES_PORT are required env variables for forming a pg connection string for the django database
POSTGRES_DB = os.environ.get('POSTGRES_DB', default=None)
POSTGRES_USER = os.environ.get('POSTGRES_USER', default=None)
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', default=None)
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', default=None)
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', default=None)

if POSTGRES_DB and POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_HOST and POSTGRES_PORT:
    DATABASES['default'] = db_url(f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

for db_key, db_dict in DATABASES.items():
    # Engine should be '.postgresql' or '.postgresql_psycopg2' for all db(s)
    if not db_dict['ENGINE'].startswith('django.db.backends.postgresql'):
        raise ValueError(
            f"{db_key} is not a PostgreSQL database. "
            f"{db_dict['ENGINE']} found for {db_key}'s engine."
        )

# pytest-django will create a new database named 'test_{DATABASES[table_db]['NAME']}'
# and use it for our API tests if we don't specify DATABASES[table_db]['TEST']['NAME']
TEST = bool(os.environ.get('TEST', default=False))
if TEST:
    for db_key, _ in [pipe_delim(i) for i in os.environ.get('MATHESAR_DATABASES', default='').split(',') if i != '']:
        DATABASES[db_key]['TEST'] = {'NAME': DATABASES[db_key]['NAME']}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default="2gr6ud88x=(p855_5nbj_+7^gw-iz&n7ldqv%94mjaecl+b9=4")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', default=False))

ALLOWED_HOSTS = [i.strip() for i in os.environ.get('ALLOWED_HOSTS', default=".localhost, 127.0.0.1, [::1]").split(',')]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/

STATIC_URL = "/static/"

# When running with DEBUG=False, the webserver needs to serve files from this location
# python manage.py collectstatic has to be run to collect all static files into this location
# The files need to served in brotli or gzip compressed format
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Media files (uploaded by the user)
DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, '.media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', default=DEFAULT_MEDIA_ROOT)

MEDIA_URL = "/media/"

# Update Authentication classes, removed BasicAuthentication
# Defaults: https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER':
        'mathesar.exception_handlers.mathesar_exception_handler',
}

# Mathesar settings
MATHESAR_MODE = os.environ.get('MODE', default='PRODUCTION')
MATHESAR_UI_BUILD_LOCATION = os.path.join(BASE_DIR, 'mathesar/static/mathesar/')
MATHESAR_MANIFEST_LOCATION = os.path.join(MATHESAR_UI_BUILD_LOCATION, 'manifest.json')
MATHESAR_CLIENT_DEV_URL = os.environ.get(
    'MATHESAR_CLIENT_DEV_URL',
    default='http://localhost:3000'
)
MATHESAR_UI_SOURCE_LOCATION = os.path.join(BASE_DIR, 'mathesar_ui/')
MATHESAR_CAPTURE_UNHANDLED_EXCEPTION = os.environ.get('CAPTURE_UNHANDLED_EXCEPTION', default=False)
MATHESAR_STATIC_NON_CODE_FILES_LOCATION = os.path.join(BASE_DIR, 'mathesar/static/non-code/')
MATHESAR_ANALYTICS_URL = os.environ.get('MATHESAR_ANALYTICS_URL', default='https://example.com')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# UI source files have to be served by Django in order for static assets to be included during dev mode
# https://vitejs.dev/guide/assets.html
# https://vitejs.dev/guide/backend-integration.html
STATICFILES_DIRS = [MATHESAR_UI_SOURCE_LOCATION, MATHESAR_STATIC_NON_CODE_FILES_LOCATION] if MATHESAR_MODE == 'DEVELOPMENT' else [MATHESAR_UI_BUILD_LOCATION, MATHESAR_STATIC_NON_CODE_FILES_LOCATION]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Accounts
AUTH_USER_MODEL = 'mathesar.User'
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_URL
DRF_ACCESS_POLICY = {
    'reusable_conditions': ['mathesar.api.permission_conditions']
}
# List of Template names that contains additional script tags to be added to the base template
BASE_TEMPLATE_ADDITIONAL_SCRIPT_TEMPLATES = []

# i18n
LANGUAGES = [
    ('en', 'English'),
    ('ja', 'Japanese'),
]
LOCALE_PATHS = [
    'translations'
]
LANGUAGE_COOKIE_NAME = 'display_language'
FALLBACK_LANGUAGE = 'en'

SALT_KEY = SECRET_KEY
