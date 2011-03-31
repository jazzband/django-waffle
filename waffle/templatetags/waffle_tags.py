from django import template

from waffle import flag_is_active, switch_is_active


register = template.Library()


class WaffleNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false, condition, name):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.condition = condition
        self.name = name

    def __repr__(self):
        return '<Waffle node: %s>' % self.name

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def render(self, context):
        if self.condition(context['request'], self.name):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


@register.tag
def waffleflag(parser, token):
    try:
        tag, flag_name = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, \
              "%r tag requires an argument" % token.contents.split()[0]

    flag_name = flag_name.strip('\'"')
    condition = lambda r, n: flag_is_active(r, n)

    nodelist_true = parser.parse(('else', 'endwaffleflag'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endwaffleflag',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return WaffleNode(nodelist_true, nodelist_false, condition, flag_name)


@register.tag
def waffleswitch(parser, token):
    try:
        tag, switch_name = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, \
              "%r tag requires an argument" % token.contents.split()[0]

    switch_name = switch_name.strip('\'"')
    condition = lambda r, n: switch_is_active(n)

    nodelist_true = parser.parse(('else', 'endwaffleswitch'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endwaffleswitch',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return WaffleNode(nodelist_true, nodelist_false, condition, switch_name)
