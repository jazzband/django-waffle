import os

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

JINJA_CONFIG = {}

SITE_ID = 1
USE_I18N = False

SECRET_KEY = 'foobar'

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    },

    # Provide a readonly DB for testing DB replication scenarios.
    'readonly': {
        'NAME': 'test.readonly.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

if 'DATABASE_URL' in os.environ:
    try:
        import dj_database_url
        import psycopg2
        DATABASES['default'] = dj_database_url.config()
    except ImportError:
        raise ImportError('Using the DATABASE_URL variable requires '
                          'dj-database-url and psycopg2. Try:\n\npip install '
                          '-r travis.txt')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'waffle',
    'test_app',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'waffle.middleware.WaffleMiddleware',
)


ROOT_URLCONF = 'test_app.urls'

_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.request',
)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_regex': r'jinja.*',
            'match_extension': '',
            'newstyle_gettext': True,
            'context_processors': _CONTEXT_PROCESSORS,
            'undefined': 'jinja2.Undefined',
            'extensions': [
                'jinja2.ext.i18n',
                'jinja2.ext.autoescape',
                'waffle.jinja.WaffleExtension',
            ],
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': _CONTEXT_PROCESSORS,
        }
    },
]

WAFFLE_FLAG_DEFAULT = False
WAFFLE_SWITCH_DEFAULT = False
WAFFLE_SAMPLE_DEFAULT = False
WAFFLE_READ_FROM_WRITE_DB = False
WAFFLE_OVERRIDE = False
WAFFLE_UNIQUE_FLAG_NAME = False
WAFFLE_CACHE_PREFIX = 'test:'
WAFFLE_FLAG_CLASS = 'test_app.models.Flag'

WAFFLE = {
    'FLAG_DEFAULT' : False,
    'SWITCH_DEFAULT' : False,
    'SAMPLE_DEFAULT' : False,
    'READ_FROM_WRITE_DB' : False,
    'OVERRIDE' : False,
    'UNIQUE_FLAG_NAME': False,
    'CACHE_PREFIX' : 'test:',
    'FLAG_CLASS': 'test_app.models.Flag',
}
