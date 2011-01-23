from django import template

from waffle import is_active


register = template.Library()


class WaffleNode(template.Node):
    def __init__(self, nodelist, flag_name):
        self.nodelist = nodelist
        self.flag_name = flag_name

    def render(self, context):
        if is_active(context['request'], self.flag_name):
            return self.nodelist.render(context)
        return ''


@register.tag
def waffle(parser, token):
    try:
        tag, flag_name = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, \
              "%r tag requires arguments" % token.contents.split()[0]

    flag_name = flag_name.strip('\'"')

    nodelist = parser.parse(('endwaffle',))
    parser.delete_first_token()

    return WaffleNode(nodelist, flag_name)
