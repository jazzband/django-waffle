from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache

from waffle import flag_is_active
from waffle.models import Flag


@never_cache
def wafflejs(request):
    flags = Flag.objects.all()
    values = [(f.name, flag_is_active(request, f.name)) for f in flags]
    return render_to_response('waffle/waffle.js', {'flags': values},
                              mimetype='application/x-javascript')
