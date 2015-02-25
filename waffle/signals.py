import django.dispatch


flag_set = django.dispatch.Signal(providing_args=['request', 'flag_name', 'active'])
