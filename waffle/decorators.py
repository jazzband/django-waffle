from functools import wraps

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.decorators import available_attrs

from waffle import flag_is_active, switch_is_active


def waffle_flag(flag_name, template_name=None):
    def decorator(view):
        @wraps(view, assigned=available_attrs(view))
        def _wrapped_view(request, *args, **kwargs):
            if flag_name.startswith('!'):
                active = not flag_is_active(request, flag_name[1:])
            else:
                active = flag_is_active(request, flag_name)

            if not active:
                if template_name:
                    return render_to_response(template_name, {
                       'flag_name': flag_name,
                    }, context_instance=RequestContext(request))
                raise Http404
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def waffle_switch(switch_name, template_name=None):
    def decorator(view):
        @wraps(view, assigned=available_attrs(view))
        def _wrapped_view(request, *args, **kwargs):
            if switch_name.startswith('!'):
                active = not switch_is_active(switch_name[1:])
            else:
                active = switch_is_active(switch_name)

            if not active:
                if template_name:
                    return render_to_response(template_name, {
                       'switch_name': switch_name,
                    }, context_instance=RequestContext(request))
                raise Http404
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
