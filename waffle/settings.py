from __future__ import unicode_literals

from django.conf import settings


CACHE_PREFIX = getattr(settings, 'WAFFLE_CACHE_PREFIX', 'waffle:')
COOKIE_NAME = getattr(settings, 'WAFFLE_COOKIE', 'dwf_%s')
TEST_COOKIE_NAME = getattr(settings, 'WAFFLE_TESTING_COOKIE', 'dwft_%s')
FLAG_CACHE_KEY = getattr(settings, 'WAFFLE_FLAG_CACHE_KEY', 'flag:%s')
FLAGS_ALL_CACHE_KEY = getattr(settings, 'WAFFLE_FLAGS_ALL_CACHE_KEY', 'flags:all')
FLAG_USERS_CACHE_KEY = getattr(settings, 'WAFFLE_FLAG_USERS_CACHE_KEY', 'flag:%s:users')
FLAG_GROUPS_CACHE_KEY = getattr(settings, 'WAFFLE_FLAG_GROUPS_CACHE_KEY', 'flag:%s:groups')
SAMPLE_CACHE_KEY = getattr(settings, 'WAFFLE_SAMPLE_CACHE_KEY', 'sample:%s')
SAMPLES_ALL_CACHE_KEY = getattr(settings, 'WAFFLE_SAMPLES_ALL_CACHE_KEY', 'samples:all')
SWITCH_CACHE_KEY = getattr(settings, 'WAFFLE_SWITCH_CACHE_KEY', 'switch:%s')
SWITCHES_ALL_CACHE_KEY = getattr(settings, 'WAFFLE_SWITCHES_ALL_CACHE_KEY', 'switches:all')


SWITCH_DEFAULT = getattr(settings, 'WAFFLE_SWITCH_DEFAULT', False)
FLAG_DEFAULT = getattr(settings, 'WAFFLE_FLAG_DEFAULT', False)
SAMPLE_DEFAULT = getattr(settings, 'WAFFLE_SAMPLE_DEFAULT', False)

SECURE = getattr(settings, 'WAFFLE_SECURE', False)
MAX_AGE = getattr(settings, 'WAFFLE_MAX_AGE', 2592000)  # 1 month
OVERRIDE = getattr(settings, 'WAFFLE_OVERRIDE', False)
