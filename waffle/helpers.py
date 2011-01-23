from jingo import register
import jinja2

from waffles import is_active


@register.function
@jinja2.contextfunction
def waffle(context, flag_name):
    return is_active(context['request'], flag_name)
