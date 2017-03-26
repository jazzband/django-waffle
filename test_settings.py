import os
import django

DJANGO_VERSION = django.VERSION

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEMPLATE_DEBUG = True
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

JINJA_CONFIG = {}

SITE_ID = 1
USE_I18N = False

SECRET_KEY = 'foobar'

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'waffle',
    'test_app',
)

_MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'waffle.middleware.WaffleMiddleware',
)


if DJANGO_VERSION < (1, 10):
    MIDDLEWARE_CLASSES = _MIDDLEWARE_CLASSES
else:
    MIDDLEWARE = _MIDDLEWARE_CLASSES

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
WAFFLE_OVERRIDE = False
WAFFLE_CACHE_PREFIX = 'test:'
