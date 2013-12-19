import django

__all__ = ['User']

# Django 1.5+ compatibility
if django.VERSION >= (1, 5):
    from django.conf import settings
    User = settings.AUTH_USER_MODEL
else:
    from django.contrib.auth.models import User
