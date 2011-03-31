from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache

from waffle import flag_is_active
from waffle.models import Flag, Switch


@never_cache
def wafflejs(request):
    flags = Flag.objects.all()
    flag_values = [(f.name, flag_is_active(request, f.name)) for f in flags]
    switches = Switch.objects.all()
    switch_values = [(s.name, s.active) for s in switches]
    return render_to_response('waffle/waffle.js', {'flags': flag_values,
                                                   'switches': switch_values},
                              mimetype='application/x-javascript')
