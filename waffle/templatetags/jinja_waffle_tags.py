import jinja2

from waffle import flag_is_active, sample_is_active, switch_is_active
from waffle.views import _generate_waffle_js


@jinja2.contextfunction
def flag_helper(context, flag_name):
    return flag_is_active(context['request'], flag_name)


@jinja2.contextfunction
def inline_wafflejs_helper(context):
    return _generate_waffle_js(context['request'])


helpers = {
    'flag': flag_helper,
    'switch': switch_is_active,
    'sample': sample_is_active,
    'wafflejs': inline_wafflejs_helper
}

try:
    import jingo

    jingo.env.globals['waffle'] = helpers
except ImportError:
    # jingo isn't being used. Move on.
    pass


try:
    from django_jinja.library import global_function

    global_function('waffle', helpers)
except ImportError:
    # django-jinja isn't being used. Move on.
    pass
