from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import never_cache

from waffle import flag_is_active, sample_is_active
from waffle.compat import cache
from waffle.models import Flag, Sample, Switch
from waffle.utils import get_setting, keyfmt


@never_cache
def wafflejs(request):
    return HttpResponse(_generate_waffle_js(request),
                        content_type='application/x-javascript')


def _generate_waffle_js(request):
    flags = cache.get(keyfmt(get_setting('ALL_FLAGS_CACHE_KEY')))
    if flags is None:
        flags = Flag.objects.values_list('name', flat=True)
        cache.add(keyfmt(get_setting('ALL_FLAGS_CACHE_KEY')), flags)
    flag_values = [(f, flag_is_active(request, f)) for f in flags]

    switches = cache.get(keyfmt(get_setting('ALL_SWITCHES_CACHE_KEY')))
    if switches is None:
        switches = Switch.objects.values_list('name', 'active')
        cache.add(keyfmt(get_setting('ALL_SWITCHES_CACHE_KEY')), switches)

    samples = cache.get(keyfmt(get_setting('ALL_SAMPLES_CACHE_KEY')))
    if samples is None:
        samples = Sample.objects.values_list('name', flat=True)
        cache.add(keyfmt(get_setting('ALL_SAMPLES_CACHE_KEY')), samples)
    sample_values = [(s, sample_is_active(s)) for s in samples]

    return loader.render_to_string('waffle/waffle.js', {
        'flags': flag_values,
        'switches': switches,
        'samples': sample_values,
        'flag_default': get_setting('FLAG_DEFAULT'),
        'switch_default': get_setting('SWITCH_DEFAULT'),
        'sample_default': get_setting('SAMPLE_DEFAULT'),
    })
