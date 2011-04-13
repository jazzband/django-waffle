from django.core.cache import cache
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache

from waffle import flag_is_active, FLAGS_ALL_CACHE_KEY, SWITCHES_ALL_CACHE_KEY
from waffle.models import Flag, Switch


@never_cache
def wafflejs(request):
    flags = cache.get(FLAGS_ALL_CACHE_KEY)
    if not flags:
        flags = Flag.objects.all().values_list('name', flat=True)
        cache.add(FLAGS_ALL_CACHE_KEY, flags)
    flag_values = [(f, flag_is_active(request, f)) for f in flags]

    switches = cache.get(SWITCHES_ALL_CACHE_KEY)
    if not switches:
        switches = Switch.objects.all().values_list('name', 'active')
        cache.add(SWITCHES_ALL_CACHE_KEY, switches)
    switch_values = [(s.name, s.active) for s in switches]
    return render_to_response('waffle/waffle.js', {'flags': flag_values,
                                                   'switches': switch_values},
                              mimetype='application/x-javascript')
