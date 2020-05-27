import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get(
    "SECRET_KEY", 'fwki09_x7z@vwb3=)egz_f==)jcj485-smpo+qp&^$7nct+s(1'
)

DEBUG = os.environ.get("DEBUG", False)
PROD = not DEBUG

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = []

AUTH_USER_MODEL = "users.MyUser"

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.flatpages',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'storages',
    'celery',
    'bootstrap_datepicker_plus',
    'ckeditor',
    'django_celery_beat',
    'social_django',
    'channels',
]

CUSTOM_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'task.apps.TaskConfig',
]

INSTALLED_APPS = THIRD_PARTY_APPS + CUSTOM_APPS + DJANGO_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'app.urls'

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
                'django.template.context_processors.i18n',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

ASGI_APPLICATION = 'app.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

SITE_ID = 1


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {},
    'db_default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', "db_default"),
        'USER': os.environ.get('POSTGRES_USER', "db_user"),
        'PASSWORD': os.environ.get(
            'POSTGRES_PASSWORD',
            "gk2ccPem87TVMvxKsCndcJyHyK5NPNUWkQXJXtwz5MyXeZjuMJPTeZkpECCT9uEZ"
        ),
        'HOST': os.environ.get('POSTGRES_HOST', "localhost"),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    },
    'db_mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', "db_mysql"),
        'USER': os.environ.get('MYSQL_USER', "db_user"),
        'PASSWORD': os.environ.get(
            'MYSQL_PASSWORD',
            "tpsAfAQPLvYkhBuztctVB9ath8ejP2yDNmUszFbsK5stg7g29QEcQMKDc3yBR9B5"
        ),
        'HOST': os.environ.get('MYSQL_HOST', "127.0.0.1"),
        'PORT': os.environ.get('MYSQL_PORT', 3306),
    }
}

DATABASE_ROUTERS = ['app.routers.DbRouter']

DATABASE_APPS_MAPPING = {
    "users": "db_default",
    'auth': "db_default",
    'admin': "db_default",
    'contenttypes': "db_default",
    'sessions': "db_default",
    'sites': "db_default",
    'social_django': "db_default",
    'flatpages': "db_default",
    'django_celery': "db_default",
    "task": "db_default",
    "core": "db_mysql",
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

TIME_ZONE = 'Asia/Baku'

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
    os.path.join(BASE_DIR, 'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

if DEBUG:  # change to PROD when in prod environment
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST_USER = os.environ.get("EMAIL_USER", "yunusovbekir@gmail.com")
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD", "fpbivjpbskawsxws")
else:
    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend",
    )

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


# Ckeditor config
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YouCustomToolbarConfig': [
            {'name': 'document',
             'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print',
                       '-', ]},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Blockquote',
                       'JustifyLeft', 'JustifyCenter',
                       'JustifyRight', 'JustifyBlock', ]},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'youcustomtools', 'items': ['Preview', 'Maximize']},
        ],
    }
}


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
