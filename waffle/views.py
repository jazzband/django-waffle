from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import never_cache

from . import (keyfmt, flag_is_active, sample_is_active, settings,
               all_flags, all_switches, all_samples)
from .models import Flag, Sample, Switch
from .compat import cache


@never_cache
def wafflejs(request):
    return HttpResponse(_generate_waffle_js(request),
                        content_type='application/x-javascript')


def _generate_waffle_js(request):
    flag_values = all_flags(request)
    switches = all_switches()
    sample_values = all_samples()

    flag_default = getattr(settings, 'WAFFLE_FLAG_DEFAULT', False)
    switch_default = getattr(settings, 'WAFFLE_SWITCH_DEFAULT', False)
    sample_default = getattr(settings, 'WAFFLE_SAMPLE_DEFAULT', False)

    return loader.render_to_string('waffle/waffle.js', {
        'flags': flag_values,
        'switches': switches,
        'samples': sample_values,
        'flag_default': flag_default,
        'switch_default': switch_default,
        'sample_default': sample_default,
    })
