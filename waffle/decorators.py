from functools import wraps

from django.http import Http404
from django.utils.decorators import available_attrs

from waffle import flag_is_active, switch_is_active


def waffle_flag(flag_name):
    def decorator(view):
        @wraps(view, assigned=available_attrs(view))
        def _wrapped_view(request, *args, **kwargs):
            if flag_name.startswith('!'):
                active = not flag_is_active(request, flag_name[1:])
            else:
                active = flag_is_active(request, flag_name)

            if not active:
                raise Http404
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def waffle_switch(switch_name):
    def decorator(view):
        @wraps(view, assigned=available_attrs(view))
        def _wrapped_view(request, *args, **kwargs):
            if switch_name.startswith('!'):
                active = not switch_is_active(switch_name[1:])
            else:
                active = switch_is_active(switch_name)

            if not active:
                raise Http404
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
