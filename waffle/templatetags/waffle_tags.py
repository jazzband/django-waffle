from __future__ import unicode_literals

from django import template
from django.template.base import VariableDoesNotExist

from waffle import flag_is_active, sample_is_active, switch_is_active
from waffle.views import _generate_waffle_js


register = template.Library()


# fake logic operator for backward compatibility with single-argument template tags
def _first(l):
    return bool(next(iter(l)))


class WaffleNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, nodelist_true, nodelist_false, condition, names,
                 compiled_names, logic_op):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.condition = condition
        self.names = names
        self.compiled_names = compiled_names
        self.logic_op = logic_op

    def __repr__(self):
        return '<Waffle node: %s>' % self.name

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def render(self, context):
        names = self.names
        for i, name in enumerate(self.compiled_names):
            try:
                tmp = name.resolve(context)
                names[i] = tmp
            except VariableDoesNotExist:
                pass  # leave unresolved

        if self.logic_op(map(lambda n: self.condition(context.get('request', None), n), names)):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

    @classmethod
    def handle_token(cls, parser, token, kind, condition, logic_op=_first):
        bits = token.split_contents()
        if len(bits) < 2:
            raise template.TemplateSyntaxError("%r tag requires an argument" %
                                               bits[0])

        names = bits[1:]
        compiled_names = map(parser.compile_filter, names)

        nodelist_true = parser.parse(('else', 'end%s' % kind))
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('end%s' % kind,))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()

        return cls(nodelist_true, nodelist_false, condition,
                   names, compiled_names, logic_op)


@register.tag
def flag(parser, token):
    return WaffleNode.handle_token(parser, token, 'flag', flag_is_active)


@register.tag
def flagany(parser, token):
    return WaffleNode.handle_token(parser, token, 'flagany', flag_is_active, any)


@register.tag
def flagall(parser, token):
    return WaffleNode.handle_token(parser, token, 'flagall', flag_is_active, all)


@register.tag
def switch(parser, token):
    return WaffleNode.handle_token(parser, token, 'switch', lambda request, name: switch_is_active(name))


@register.tag
def switchany(parser, token):
    return WaffleNode.handle_token(parser, token, 'switchany', lambda request, name: switch_is_active(name), any)


@register.tag
def switchall(parser, token):
    return WaffleNode.handle_token(parser, token, 'switchall', lambda request, name: switch_is_active(name), all)


@register.tag
def sample(parser, token):
    return WaffleNode.handle_token(parser, token, 'sample', lambda request, name: sample_is_active(name))


@register.tag
def sampleany(parser, token):
    return WaffleNode.handle_token(parser, token, 'sampleany', lambda request, name: sample_is_active(name), any)


@register.tag
def sampleall(parser, token):
    return WaffleNode.handle_token(parser, token, 'sampleall', lambda request, name: sample_is_active(name), all)


class InlineWaffleJSNode(template.Node):
    def render(self, context):
        return _generate_waffle_js(context['request'])


@register.tag
def wafflejs(parser, token):
    return InlineWaffleJSNode()
