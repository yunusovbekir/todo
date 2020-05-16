import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fwki09_x7z@vwb3=)egz_f==)jcj485-smpo+qp&^$7nct+s(1'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = not os.environ.get("DEBUG", False)
# PROD = not DEBUG
DEBUG = True
PROD = not DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'bootstrap_datepicker_plus',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'celery',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.flatpages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'task/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

SITE_ID = 3


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', "db_name"),
        'USER': os.environ.get('POSTGRES_USER', "db_user"),
        'PASSWORD': os.environ.get(
            'POSTGRES_PASSWORD',
            "gk2ccPem87TVMvxKsCndcJyHyK5NPNUWkQXJXtwz5MyXeZjuMJPTeZkpECCT9uEZ"
        ),
        'HOST': os.environ.get('POSTGRES_HOST', "localhost"),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
if PROD:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'task/templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}


CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'tasks-explore'
LOGIN_URL = 'login'

if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST_USER = os.environ.get("email_user", "user")
    EMAIL_HOST = "smtp.domain.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get("email_password", "password")
else:
    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend"
    )


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

LOG_LEVEL = 'ERROR' if PROD else 'DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': not DEBUG,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:=> %(message)s',
        },
        'focused': {
            'format': '\n----------------------\n%(asctime)s [%(levelname)s] %(name)s:=> %(message)s \n----------------------',
        },
    },
    'handlers': {
        'my_custom_debug': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'focused',
        },
        'request_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['my_custom_debug'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}
