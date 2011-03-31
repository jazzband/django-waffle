from jingo import register
import jinja2

from waffle import flag_is_active, switch_is_active


@register.function
@jinja2.contextfunction
def waffle_flag(context, flag_name):
    return flag_is_active(context['request'], flag_name)


@register.function
def waffle_switch(switch_name):
    return switch_is_active(switch_name)
