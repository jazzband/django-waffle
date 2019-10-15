from django.apps import AppConfig


class WaffleConfig(AppConfig):
    name = 'waffle'
    verbose_name = 'django-waffle'

    def ready(self):
        import waffle.signals  # noqa: F401
