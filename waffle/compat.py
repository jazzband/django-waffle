import django

__all__ = ['AUTH_USER_MODEL']

# Django 1.5+ compatibility
if django.VERSION >= (1, 5):
    from django.conf import settings
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
else:
    AUTH_USER_MODEL = 'auth.User'
