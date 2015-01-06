from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import never_cache

from . import (keyfmt, flags_are_active, sample_is_active, settings)
from .models import Flag, Sample, Switch
from .compat import cache


@never_cache
def wafflejs(request):
    return HttpResponse(_generate_waffle_js(request),
                        content_type='application/x-javascript')


def _generate_waffle_js(request):
    flags = cache.get(keyfmt(settings.FLAGS_ALL_CACHE_KEY))
    if flags is None:
        flags = Flag.objects.values_list('name', flat=True)
        cache.add(keyfmt(settings.FLAGS_ALL_CACHE_KEY), flags)
    flag_values = flags_are_active(flags, request)

    switches = cache.get(keyfmt(settings.SWITCHES_ALL_CACHE_KEY))
    if switches is None:
        switches = Switch.objects.values_list('name', 'active')
        cache.add(keyfmt(settings.SWITCHES_ALL_CACHE_KEY), switches)

    samples = cache.get(keyfmt(settings.SAMPLES_ALL_CACHE_KEY))
    if samples is None:
        samples = Sample.objects.values_list('name', flat=True)
        cache.add(keyfmt(settings.SAMPLES_ALL_CACHE_KEY), samples)
    sample_values = [(s, sample_is_active(s)) for s in samples]

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
