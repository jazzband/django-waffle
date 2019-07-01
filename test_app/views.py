from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View

from waffle import flag_is_active
from waffle.decorators import waffle_flag, waffle_switch
from waffle.mixins import WaffleFlagMixin, WaffleSampleMixin, WaffleSwitchMixin


def flag_in_view(request):
    if flag_is_active(request, 'myflag'):
        return HttpResponse('on')
    return HttpResponse('off')


def flag_in_jinja(request):
    return render(request, 'jinja/jinja.html')


def flag_in_django(request):
    context = {
        'flag_var': 'flag_var',
        'switch_var': 'switch_var',
        'sample_var': 'sample_var',
    }
    return render(request, 'django/django.html', context=context)


def no_request_context(request):
    return render_to_string('django/django_email.html', context={})


@waffle_switch('foo')
def switched_view(request):
    return HttpResponse('foo')


@waffle_switch('!foo')
def switched_off_view(request):
    return HttpResponse('foo')


@waffle_flag('foo')
def flagged_view(request):
    return HttpResponse('foo')


@waffle_flag('!foo')
def flagged_off_view(request):
    return HttpResponse('foo')


def foo_view(request):
    return HttpResponse('redirected')


def foo_view_with_args(request, some_number):
    return HttpResponse('redirected with {}'.format(some_number))


@waffle_switch('foo', redirect_to=foo_view)
def switched_view_with_valid_redirect(request):
    return HttpResponse('foo')


@waffle_switch('foo', redirect_to='foo_view')
def switched_view_with_valid_url_name(request):
    return HttpResponse('foo')


@waffle_switch('foo', redirect_to=foo_view_with_args)
def switched_view_with_args_with_valid_redirect(request, some_number):
    return HttpResponse('foo with {}'.format(some_number))


@waffle_switch('foo', redirect_to='foo_view_with_args')
def switched_view_with_args_with_valid_url_name(request, some_number):
    return HttpResponse('foo with {}'.format(some_number))


@waffle_switch('foo', redirect_to='invalid_view')
def switched_view_with_invalid_redirect(request):
    return HttpResponse('foo')


@waffle_flag('foo', redirect_to=foo_view)
def flagged_view_with_valid_redirect(request):
    return HttpResponse('foo')


@waffle_flag('foo', redirect_to='foo_view')
def flagged_view_with_valid_url_name(request):
    return HttpResponse('foo')


@waffle_flag('foo', redirect_to=foo_view_with_args)
def flagged_view_with_args_with_valid_redirect(request, some_number):
    return HttpResponse('foo with {}'.format(some_number))


@waffle_flag('foo', redirect_to='foo_view_with_args')
def flagged_view_with_args_with_valid_url_name(request, some_number):
    return HttpResponse('foo with {}'.format(some_number))


@waffle_flag('foo', redirect_to='invalid_view')
def flagged_view_with_invalid_redirect(request):
    return HttpResponse('foo')


class BaseWaffleView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('foo')


class FlagView(WaffleFlagMixin, BaseWaffleView):
    waffle_flag = 'foo'


class FlagOffView(WaffleFlagMixin, BaseWaffleView):
    waffle_flag = '!foo'


class SampleView(WaffleSampleMixin, BaseWaffleView):
    waffle_sample = 'foo'


class SampleOffView(WaffleSampleMixin, BaseWaffleView):
    waffle_sample = '!foo'


class SwitchView(WaffleSwitchMixin, BaseWaffleView):
    waffle_switch = 'foo'


class SwitchOffView(WaffleSwitchMixin, BaseWaffleView):
    waffle_switch = '!foo'
