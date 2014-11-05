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

TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

JINGO_EXCLUDE_APPS = (
    'django',
    'waffle',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

WAFFLE_FLAG_DEFAULT = False
WAFFLE_SWITCH_DEFAULT = False
WAFFLE_SAMPLE_DEFAULT = False
WAFFLE_OVERRIDE = False

if django.VERSION < (1, 7):
    INSTALLED_APPS += ('south', )

    SOUTH_MIGRATION_MODULES = {
        'waffle': 'waffle.south_migrations'
    }
