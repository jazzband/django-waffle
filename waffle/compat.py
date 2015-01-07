import django
from django.conf import settings

__all__ = ['cache']

if hasattr(settings, 'WAFFLE_CACHE_NAME'):
    cache_name = settings.WAFFLE_CACHE_NAME
    if django.VERSION >= (1, 7):
        from django.core.cache import caches
        cache = caches[cache_name]
    else:
        from django.core.cache import get_cache
        cache = get_cache(cache_name)
else:
    from django.core.cache import cache

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
