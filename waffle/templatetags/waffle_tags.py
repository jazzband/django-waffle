from django import template

from waffle import is_active


register = template.Library()


class WaffleNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false, flag_name):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.flag_name = flag_name

    def __repr__(self):
        return '<Waffle node: %s>' % self.flag_name

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def render(self, context):
        if is_active(context['request'], self.flag_name):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


@register.tag
def waffle(parser, token):
    try:
        tag, flag_name = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, \
              "%r tag requires an argument" % token.contents.split()[0]

    flag_name = flag_name.strip('\'"')

    nodelist_true = parser.parse(('else', 'endwaffle'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endwaffle',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return WaffleNode(nodelist_true, nodelist_false, flag_name)
