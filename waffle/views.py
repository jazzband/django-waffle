from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import never_cache

from waffle import flag_is_active, sample_is_active
from waffle.models import Flag, Sample, Switch
from waffle.utils import get_setting, keyfmt, get_cache


cache = get_cache()


@never_cache
def wafflejs(request):
    return HttpResponse(_generate_waffle_js(request),
                        content_type='application/x-javascript')


def _generate_waffle_js(request):
    flags = Flag.get_all()
    flag_values = [(f.name, f.is_active(request)) for f in flags]

    switches = Switch.get_all()
    switch_values = [(s.name, s.is_active()) for s in switches]

    samples = Sample.get_all()
    sample_values = [(s.name, s.is_active()) for s in samples]

    return loader.render_to_string('waffle/waffle.js', {
        'flags': flag_values,
        'switches': switch_values,
        'samples': sample_values,
        'flag_default': get_setting('FLAG_DEFAULT'),
        'switch_default': get_setting('SWITCH_DEFAULT'),
        'sample_default': get_setting('SAMPLE_DEFAULT'),
    })
