from jingo import register
import jinja2

from waffle import flag_is_active


@register.function
@jinja2.contextfunction
def waffle(context, flag_name):
    return flag_is_active(context['request'], flag_name)
