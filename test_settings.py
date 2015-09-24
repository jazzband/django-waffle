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

if django.VERSION < (1,8):
    # Old style TEMPLATE_* settings.
    # Use jingo.

    TEMPLATE_LOADERS = (
        'jingo.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.request',
    )

    JINGO_EXCLUDE_APPS = (
        'django',
        'waffle',
    )

else:
    # New style TEMPLATES setting.
    # Use django-jinja

    INSTALLED_APPS += ('django_jinja', )

    TEMPLATES = [
        # Configure the Jinja2 template engine
        {
            'BACKEND': 'django_jinja.backend.Jinja2',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                "match_regex": r"jingo.*",
                'match_extension': '',
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'extensions': [
                    'jinja2.ext.i18n',
                    'jinja2.ext.autoescape',
                    'jinja2.ext.with_',
                    'jinja2.ext.do'
                ]
            }
        },
        # Configure the Django template engine
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
                ],
            },
        },
    ]
