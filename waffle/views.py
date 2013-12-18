from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import never_cache

from waffle import (keyfmt, flag_is_active, sample_is_active,
                    FLAGS_ALL_CACHE_KEY, SWITCHES_ALL_CACHE_KEY,
                    SAMPLES_ALL_CACHE_KEY)
from waffle.models import Flag, Sample, Switch
from django.conf import settings


@never_cache
def wafflejs(request):
    return HttpResponse(_generate_waffle_js(request),
                       mimetype='application/x-javascript')


def _generate_waffle_js(request):
    flags = cache.get(keyfmt(FLAGS_ALL_CACHE_KEY))
    if not flags:
        flags = Flag.objects.values_list('name', flat=True)
        cache.add(keyfmt(FLAGS_ALL_CACHE_KEY), flags)
    flag_values = [(f, flag_is_active(request, f)) for f in flags]

    switches = cache.get(keyfmt(SWITCHES_ALL_CACHE_KEY))
    if not switches:
        switches = Switch.objects.values_list('name', 'active')
        cache.add(keyfmt(SWITCHES_ALL_CACHE_KEY), switches)

    samples = cache.get(keyfmt(SAMPLES_ALL_CACHE_KEY))
    if not samples:
        samples = Sample.objects.values_list('name', flat=True)
        cache.add(keyfmt(SAMPLES_ALL_CACHE_KEY), samples)
    sample_values = [(s, sample_is_active(s)) for s in samples]

    flag_default = getattr(settings, 'WAFFLE_FLAG_DEFAULT', False)
    switch_default = getattr(settings, 'WAFFLE_SWITCH_DEFAULT', False)
    sample_default = getattr(settings, 'WAFFLE_SAMPLE_DEFAULT', False)

    return loader.render_to_string('waffle/waffle.js',
                              {
                                'flags': flag_values,
                                'switches': switches,
                                'samples': sample_values,
                                'flag_default': flag_default,
                                'switch_default': switch_default,
                                'sample_default': sample_default,
                              })
