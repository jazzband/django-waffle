from __future__ import unicode_literals

import jinja2
from jinja2.ext import Extension

from waffle import flag_is_active, sample_is_active, switch_is_active
from waffle.views import _generate_waffle_js


@jinja2.contextfunction
def flag_helper(context, flag_name):
    return flag_is_active(context['request'], flag_name)


@jinja2.contextfunction
def inline_wafflejs_helper(context):
    return _generate_waffle_js(context['request'])


class WaffleExtension(Extension):
    def __init__(self, environment):
        environment.globals['waffle'] = {
            'flag': flag_helper,
            'switch': switch_is_active,
            'sample': sample_is_active,
            'wafflejs': inline_wafflejs_helper
        }
