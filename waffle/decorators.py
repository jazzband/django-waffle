from functools import wraps

from django.http import Http404
from django.utils.decorators import available_attrs

from waffle import is_active


def waffle(flag_name):
    def decorator(view):
        if flag_name.startswith('!'):
            active = is_active(request, flag_name[1:])
        else:
            active = is_active(request, flag_name)

        @wraps(view, assigned=available_attrs(view))
        def _wrapped_view(request, *args, **kwargs):
            if not active:
                raise Http404
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
