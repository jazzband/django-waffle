import os
import django

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEMPLATE_DEBUG = True

if django.VERSION < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
else:
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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'test_app.urls'

_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

if django.VERSION <= (1, 7):
    TEMPLATE_CONTEXT_PROCESSORS = _CONTEXT_PROCESSORS

    TEMPLATE_LOADERS = (
        'jingo.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    JINGO_EXCLUDE_APPS = (
        'django',
        'waffle',
    )

    JINJA_CONFIG = {
        'extensions': [
            'jinja2.ext.autoescape',
            'waffle.jinja.WaffleExtension',
        ],
    }

else:
    TEMPLATES = [
        {
            'BACKEND': 'django_jinja.backend.Jinja2',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'match_regex': r'jingo.*',
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

if django.VERSION < (1, 7):
    INSTALLED_APPS += ('south', )

    SOUTH_MIGRATION_MODULES = {
        'waffle': 'waffle.south_migrations'
    }
