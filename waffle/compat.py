import django
from django.conf import settings

__all__ = ['User', 'get_user_model']

# Django 1.5+ compatibility
if django.VERSION >= (1, 5):
    from django.contrib.auth import get_user_model

    User = get_user_model()
else:
    from django.contrib.auth.models import User

    def get_user_model():
        return User

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
