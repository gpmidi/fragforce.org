"""
Django settings for fforg project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from datetime import timedelta

import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', 'True').lower() == 'true')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')
if SECRET_KEY == 'INSECURE':
    if DEBUG:
        import warnings

        warnings.warn('INSECURE SECRET_KEY!', RuntimeWarning)
    else:
        raise ValueError("SECRET_KEY env var must be defined when not in DEBUG=True")

# FIXME: Add LOGZ.IO Logging
LOGZIO_API_KEY = os.environ.get('LOGZIO_API_KEY', None)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'memoize',
    'ffsite',
    'ffsfdc',
    'ffdonations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fforg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ffsite.ctx.common_org',
                'ffdonations.ctx.donations',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'fforg.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'hc': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db-hc.sqlite3'),
    },
}
DATABASE_ROUTERS = ["fforg.router.HCRouter", ]
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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))
DATABASES['hc'].update(dj_database_url.config(conn_max_age=500, ssl_require=True, env="HC_RO_URL"))
try:
    DATABASES['default']['OPTIONS']['options'] = '-c search_path=%s,%s' % (
        os.environ.get('DATABASE_SCHEMA', 'public'),
        os.environ.get('HC_RO_SCHEMA', 'org'),
    )
    DATABASES['hc']['OPTIONS']['options'] = '-c search_path=%s,%s' % (
        os.environ.get('HC_RO_SCHEMA', 'org'),
        os.environ.get('DATABASE_SCHEMA', 'public'),
    )
except KeyError as e:
    pass

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_SSL_REDIRECT = True

# Heroku auto set
HEROKU_APP_ID = os.environ.get('HEROKU_APP_ID', None)
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
HEROKU_RELEASE_CREATED_AT = os.environ.get('HEROKU_RELEASE_CREATED_AT', None)
HEROKU_RELEASE_VERSION = os.environ.get('HEROKU_RELEASE_VERSION', 'v1')
HEROKU_RELEASE_VERSION_NUM = int(HEROKU_RELEASE_VERSION.lstrip('v'))
HEROKU_SLUG_COMMIT = os.environ.get('HEROKU_SLUG_COMMIT', None)
HEROKU_SLUG_DESCRIPTION = os.environ.get('HEROKU_SLUG_DESCRIPTION', None)

SINGAPORE_DONATIONS = float(os.environ.get('SINGAPORE_DONATIONS', '0.0'))
OTHER_DONATIONS = float(os.environ.get('OTHER_DONATIONS', '0.0'))
TARGET_DONATIONS = float(os.environ.get('TARGET_DONATIONS', '1.0'))

# Cache version prefix
VERSION = int(HEROKU_RELEASE_VERSION_NUM)

# Max rows for api to return
MAX_API_ROWS = int(os.environ.get('MAX_API_ROWS', 1024))

if os.environ.get('REDIS_URL', None):
    REDIS_URL_DEFAULT = 'redis://localhost'
    # Base URL - Needs DB ID added
    REDIS_URL_BASE = os.environ.get('REDIS_URL', REDIS_URL_DEFAULT)
    # Don't use DB 0 for anything
    REDIS_URL_DEFAULT = REDIS_URL_BASE + "/0"
    # Celery tasks
    REDIS_URL_TASKS = REDIS_URL_BASE + "/1"
    # Celery tombstones (aka results)
    REDIS_URL_TOMBS = REDIS_URL_BASE + "/2"
    # Misc timers
    REDIS_URL_TIMERS = REDIS_URL_BASE + "/3"
    # Django cache
    REDIS_URL_DJ_CACHE = REDIS_URL_BASE + "/4"


elif os.environ.get('REDIS0_URL', None):
    REDIS_URL_DEFAULT = 'redis://localhost'
    # Base URL - Needs DB ID added
    REDIS_URL_BASE = REDIS_URL_DEFAULT
    # Don't use DB 0 for anything
    REDIS_URL_DEFAULT = os.environ.get('REDIS0_URL', 'redis://localhost') + "/0"
    # Celery tasks
    REDIS_URL_TASKS = os.environ.get('REDIS1_URL', 'redis://localhost') + "/0"
    # Celery tombstones (aka results)
    REDIS_URL_TOMBS = os.environ.get('REDIS2_URL', 'redis://localhost') + "/0"
    # Misc timers
    REDIS_URL_TIMERS = os.environ.get('REDIS3_URL', 'redis://localhost') + "/0"
    # Django cache
    REDIS_URL_DJ_CACHE = os.environ.get('REDIS4_URL', 'redis://localhost') + "/0"

else:
    REDIS_URL_DEFAULT = 'redis://localhost'
    # Base URL - Needs DB ID added
    REDIS_URL_BASE = REDIS_URL_DEFAULT
    # Don't use DB 0 for anything
    REDIS_URL_DEFAULT = os.environ.get('REDIS0_URL', 'redis://localhost') + "/0"
    # Celery tasks
    REDIS_URL_TASKS = os.environ.get('REDIS1_URL', 'redis://localhost') + "/0"
    # Celery tombstones (aka results)
    REDIS_URL_TOMBS = os.environ.get('REDIS2_URL', 'redis://localhost') + "/0"
    # Misc timers
    REDIS_URL_TIMERS = os.environ.get('REDIS3_URL', 'redis://localhost') + "/0"
    # Django cache
    REDIS_URL_DJ_CACHE = os.environ.get('REDIS4_URL', 'redis://localhost') + "/0"

CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_ACKS_LATE = True
CELERY_BROKER_URL = REDIS_URL_TASKS
CELERY_RESULT_BACKEND = REDIS_URL_TOMBS
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', None)
MAX_UPCOMING_EVENTS = int(os.environ.get('MAX_UPCOMING_EVENTS', 20))
MAX_PAST_EVENTS = int(os.environ.get('MAX_PAST_EVENTS', 20))
MAX_ALL_EVENTS = int(os.environ.get('MAX_ALL_EVENTS', 20))
TILTIFY_TOKEN = os.environ.get('TILTIFY_TOKEN', None)
TILTIFY_TIMEOUT = int(os.environ.get('TILTIFY_TIMEOUT', 60))
TILTIFY_APP_OWNER = os.environ.get('TILTIFY_APP_OWNER', HEROKU_APP_NAME)

# Various view cache timeouts
VIEW_TEAMS_CACHE = int(os.environ.get('VIEW_TEAMS_CACHE', 20))
VIEW_PARTICIPANTS_CACHE = int(os.environ.get('VIEW_PARTICIPANTS_CACHE', 20))
VIEW_DONATIONS_CACHE = int(os.environ.get('VIEW_DONATIONS_CACHE', 20))
VIEW_DONATIONS_STATS_CACHE = int(os.environ.get('VIEW_DONATIONS_STATS_CACHE', 20))
VIEW_SITE_EVENT_CACHE = int(os.environ.get('VIEW_SITE_EVENT_CACHE', 60))
VIEW_SITE_SITE_CACHE = int(os.environ.get('VIEW_SITE_SITE_CACHE', 60))
VIEW_SITE_STATIC_CACHE = int(os.environ.get('VIEW_SITE_STATIC_CACHE', 300))

# Min time between team updates - Only cares about tracked teams!
EL_TEAM_UPDATE_FREQUENCY_MIN = timedelta(minutes=int(os.environ.get('EL_TEAM_UPDATE_FREQUENCY_MIN', 30)))
# Max time between updates for any given team - Only cares about tracked teams!
EL_TEAM_UPDATE_FREQUENCY_MAX = timedelta(minutes=int(os.environ.get('EL_TEAM_UPDATE_FREQUENCY_MAX', 120)))
# How often to check for updates
EL_TEAM_UPDATE_FREQUENCY_CHECK = timedelta(minutes=int(os.environ.get('EL_TEAM_UPDATE_FREQUENCY_CHECK', 5)))

# Min time between participants updates - Only cares about tracked participants!
EL_PTCP_UPDATE_FREQUENCY_MIN = timedelta(minutes=int(os.environ.get('EL_PTCP_UPDATE_FREQUENCY_MIN', 120)))
# Max time between updates for any given participants - Only cares about tracked participants!
EL_PTCP_UPDATE_FREQUENCY_MAX = timedelta(minutes=int(os.environ.get('EL_PTCP_UPDATE_FREQUENCY_MAX', 300)))
# How often to check for updates
EL_PTCP_UPDATE_FREQUENCY_CHECK = timedelta(minutes=int(os.environ.get('EL_PTCP_UPDATE_FREQUENCY_CHECK', 30)))

# Min time between donation list updates - Only cares about tracked teams/participants!
EL_DON_UPDATE_FREQUENCY_MIN = timedelta(minutes=int(os.environ.get('EL_DON_UPDATE_FREQUENCY_MIN', 60)))
# Max time between updates for any given donation list - Only cares about tracked teams/participants!
EL_DON_UPDATE_FREQUENCY_MAX = timedelta(minutes=int(os.environ.get('EL_DON_UPDATE_FREQUENCY_MAX', 300)))
# How often to check for updates
EL_DON_UPDATE_FREQUENCY_CHECK = timedelta(minutes=int(os.environ.get('EL_DON_UPDATE_FREQUENCY_CHECK', 15)))

# Min time between donation list updates for a team - Only cares about tracked teams
EL_DON_TEAM_UPDATE_FREQUENCY_MIN = timedelta(minutes=int(os.environ.get('EL_DON_TEAM_UPDATE_FREQUENCY_MIN', 5)))
# Max time between updates of donations for any given team - Only cares about tracked teams
EL_DON_TEAM_UPDATE_FREQUENCY_MAX = timedelta(minutes=int(os.environ.get('EL_DON_TEAM_UPDATE_FREQUENCY_MAX', 15)))

# Min time between donation list updates for a participants - Only cares about tracked participants
EL_DON_PTCP_UPDATE_FREQUENCY_MIN = timedelta(minutes=int(os.environ.get('EL_DON_PTCP_UPDATE_FREQUENCY_MIN', 5)))
# Max time between updates of donations for any given participants - Only cares about tracked participants
EL_DON_PTCP_UPDATE_FREQUENCY_MAX = timedelta(minutes=int(os.environ.get('EL_DON_PTCP_UPDATE_FREQUENCY_MAX', 15)))

# Min time between EL REST requests
EL_REQUEST_MIN_TIME = timedelta(seconds=int(os.environ.get('EL_REQUEST_MIN_TIME_SECONDS', 5)))
# Min time between EL REST requests for any given URL
EL_REQUEST_MIN_TIME_URL = timedelta(seconds=int(os.environ.get('EL_REQUEST_MIN_TIME_URL_SECONDS', 15)))
# Min time between request for any given remote host
REQUEST_MIN_TIME_HOST = timedelta(seconds=int(os.environ.get('REQUEST_MIN_TIME_HOST_SECONDS', 1)))

# How often to check for updates
TIL_TEAMS_UPDATE_FREQUENCY_CHECK = timedelta(minutes=int(os.environ.get('TIL_TEAMS_UPDATE_FREQUENCY_CHECK', 10)))
UNIV_UPDATE_FREQUENCY = timedelta(seconds=int(os.environ.get('UNIV_UPDATE_FREQUENCY', 5)))

# How long to wait in seconds after getting a parent before fetching any children
TF_UPDATE_WAIT = timedelta(seconds=int(os.environ.get('TF_UPDATE_WAIT', 120)))

# Comma seperated list of tiltify teams (the slugs or IDs) to monitor
TILTIFY_TEAMS = os.environ.get('TILTIFY_TEAMS', 'fragforce').split(',')

# Cache Configuration
if REDIS_URL_BASE and REDIS_URL_BASE == REDIS_URL_DEFAULT:
    # Dev and release config
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }
else:
    def make_key_hash(key, key_prefix, version):
        """ Create a hashed key"""
        import hashlib
        m = hashlib.sha512()
        m.update(':'.join([key_prefix, str(version), key]))
        return m.hexdigest()


    def make_key_nohash(key, key_prefix, version):
        return ':'.join([key_prefix, str(version), key])


    if os.environ.get('DJANGO_CACHE_HASH', 'false').lower() == 'true':
        make_key = make_key_hash
    else:
        make_key = make_key_nohash

    # Real config
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': REDIS_URL_DJ_CACHE,
            'TIMEOUT': int(os.environ.get('REDIS_DJ_TIMEOUT', 300)),
            'OPTIONS': {
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'SOCKET_TIMEOUT': int(os.environ.get('REDIS_DJ_SOCKET_TIMEOUT', 5)),
                'SOCKET_CONNECT_TIMEOUT': int(os.environ.get('REDIS_DJ_SOCKET_CONNECT_TIMEOUT', 3)),
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': int(os.environ.get('REDIS_DJ_POOL_MAX_CONN', 5)),
                    'timeout': int(os.environ.get('REDIS_DJ_POOL_TIMEOUT', 3)),
                },
                # 'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
                # 'SERIALIZER_CLASS_KWARGS': {},
                # Used to auto flush cache when new builds happen :-D
                'VERSION': HEROKU_RELEASE_VERSION_NUM,
                'KEY_PREFIX': '_'.join([str(HEROKU_APP_ID), str(HEROKU_APP_NAME)]),
                'KEY_FUNCTION': make_key,
            },
        },
    }

    if os.environ.get('DJANGO_COMPRESS_REDIS', 'false').lower() == 'true':
        CACHES['default']['OPTIONS']['COMPRESSOR_CLASS'] = 'redis_cache.compressors.ZLibCompressor'
        CACHES['default']['OPTIONS']['COMPRESSOR_CLASS_KWARGS'] = {
            # level = 0 - 9
            # 0 - no compression
            # 1 - fastest, biggest
            # 9 - slowest, smallest
            'level': int(os.environ.get('DJANGO_COMPRESS_REDIS_ZLIB_LEVEL', 1)),
        }

# Second to last
CELERY_BEAT_SCHEDULE = {
    'update-all-teams': {
        'task': 'ffdonations.tasks.teams.update_teams_if_needed',
        'schedule': EL_TEAM_UPDATE_FREQUENCY_CHECK,
    },
    'update-all-participants': {
        'task': 'ffdonations.tasks.participants.update_participants_if_needed',
        'schedule': EL_PTCP_UPDATE_FREQUENCY_CHECK,
    },
    'update-all-donations': {
        'task': 'ffdonations.tasks.donations.update_donations_if_needed',
        'schedule': EL_DON_UPDATE_FREQUENCY_CHECK,
    },
    'til-update-all-teams': {
        'task': 'ffdonations.tasks.tiltify.teams.update_teams',
        'schedule': TIL_TEAMS_UPDATE_FREQUENCY_CHECK,
    },
    'univ-load-el': {
        'task': 'ffdonations.tasks.univ.loaders.load_extralife',
        'schedule': UNIV_UPDATE_FREQUENCY,
    },
    'univ-load-cp': {
        'task': 'ffdonations.tasks.univ.loaders.load_childsplay',
        'schedule': UNIV_UPDATE_FREQUENCY,
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'logzioFormat': {
            'format': '{"source": "django"}'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose'
        },
        'logzio': {
            'class': 'logzio.handler.LogzioHandler',
            'level': 'DEBUG',
            'formatter': 'logzioFormat',
            'token': LOGZIO_API_KEY,
            'logzio_type': "django",
            'logs_drain_timeout': 5,
            'url': 'https://listener.logz.io:8071',
            'debug': True
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logzio'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'root': {
            'handlers': ['console', 'logzio'],
            # 'level': 'INFO'
        },
        '': {
            'handlers': ['console', 'logzio'],
            # 'level': 'INFO'
        },
    }
}

# Activate Django-Heroku - Very last
django_heroku.settings(locals())
