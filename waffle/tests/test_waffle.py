import random

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, Group, User

import mock
from nose.tools import eq_
from test_utils import RequestFactory, TestCase

from test_app import views
import waffle
from waffle.middleware import WaffleMiddleware
from waffle.models import Flag, Sample, Switch


def get(**kw):
    request = RequestFactory().get('/foo', data=kw)
    request.user = AnonymousUser()
    return request


def process_request(request, view):
    response = view(request)
    return WaffleMiddleware().process_response(request, response)


class WaffleTests(TestCase):
    def test_persist_active_flag(self):
        Flag.objects.create(name='myflag', percent='0.1')
        request = get()

        # Flag stays on.
        request.COOKIES['dwf_myflag'] = 'True'
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert 'dwf_myflag' in response.cookies
        eq_('True', response.cookies['dwf_myflag'].value)

    def test_persist_inactive_flag(self):
        Flag.objects.create(name='myflag', percent='99.9')
        request = get()

        # Flag stays off.
        request.COOKIES['dwf_myflag'] = 'False'
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert 'dwf_myflag' in response.cookies
        eq_('False', response.cookies['dwf_myflag'].value)

    def test_no_set_unused_flag(self):
        """An unused flag shouldn't have its cookie reset."""
        request = get()
        request.COOKIES['dwf_unused'] = 'True'
        response = process_request(request, views.flag_in_view)
        assert not 'dwf_unused' in response.cookies

    def test_superuser(self):
        """Test the superuser switch."""
        Flag.objects.create(name='myflag', superusers=True)
        request = get()
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

        superuser = User(username='foo', is_superuser=True)
        request.user = superuser
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

        non_superuser = User(username='bar', is_superuser=False)
        request.user = non_superuser
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_staff(self):
        """Test the staff switch."""
        Flag.objects.create(name='myflag', staff=True)
        request = get()
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

        staff = User(username='foo', is_staff=True)
        request.user = staff
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

        non_staff = User(username='foo', is_staff=False)
        request.user = non_staff
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_user(self):
        """Test the per-user switch."""
        user = User.objects.create(username='foo')
        flag = Flag.objects.create(name='myflag')
        flag.users.add(user)

        request = get()
        request.user = user
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

        request.user = User(username='someone_else')
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_group(self):
        """Test the per-group switch."""
        group = Group.objects.create(name='foo')
        user = User.objects.create(username='bar')
        user.groups.add(group)

        flag = Flag.objects.create(name='myflag')
        flag.groups.add(group)

        request = get()
        request.user = user
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

        request.user = User(username='someone_else')
        request.user.save()
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_authenticated(self):
        """Test the authenticated/anonymous switch."""
        Flag.objects.create(name='myflag', authenticated=True)

        request = get()
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

        request.user = User(username='foo')
        assert request.user.is_authenticated()
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_everyone_on(self):
        """Test the 'everyone' switch on."""
        Flag.objects.create(name='myflag', everyone=True)

        request = get()
        request.COOKIES['dwf_myflag'] = 'False'
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

        request.user = User(username='foo')
        assert request.user.is_authenticated()
        response = process_request(request, views.flag_in_view)
        eq_('on', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_everyone_off(self):
        """Test the 'everyone' switch off."""
        Flag.objects.create(name='myflag', everyone=False,
                            authenticated=True)

        request = get()
        request.COOKIES['dwf_myflag'] = 'True'
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

        request.user = User(username='foo')
        assert request.user.is_authenticated()
        response = process_request(request, views.flag_in_view)
        eq_('off', response.content)
        assert not 'dwf_myflag' in response.cookies

    def test_percent(self):
        """If you have no cookie, you get a cookie!"""
        Flag.objects.create(name='myflag', percent='50.0')
        request = get()
        response = process_request(request, views.flag_in_view)
        assert 'dwf_myflag' in response.cookies

    @mock.patch.object(random, 'uniform')
    def test_reroll(self, uniform):
        """Even without a cookie, calling flag_is_active twice should return
        the same value."""
        Flag.objects.create(name='myflag', percent='50.0')
        # Make sure we're not really random.
        request = get()  # Create a clean request.
        assert not hasattr(request, 'waffles')
        uniform.return_value = '10'  # < 50. Flag is True.
        assert waffle.flag_is_active(request, 'myflag')
        assert hasattr(request, 'waffles')  # We should record this flag.
        assert 'myflag' in request.waffles
        assert request.waffles['myflag'][0]
        uniform.return_value = '70'  # > 50. Normally, Flag would be False.
        assert waffle.flag_is_active(request, 'myflag')
        assert request.waffles['myflag'][0]

    def test_undefined(self):
        """Undefined flags are always false."""
        request = get()
        assert not waffle.flag_is_active(request, 'foo')

    @mock.patch.object(settings._wrapped, 'WAFFLE_FLAG_DEFAULT', True)
    def test_undefined_default(self):
        """WAFFLE_FLAG_DEFAULT controls undefined flags."""
        request = get()
        assert waffle.flag_is_active(request, 'foo')

    @mock.patch.object(settings._wrapped, 'WAFFLE_OVERRIDE', True)
    def test_override(self):
        request = get(foo='1')
        Flag.objects.create(name='foo')  # Off for everyone.
        assert waffle.flag_is_active(request, 'foo')

    def test_testing_flag(self):
        Flag.objects.create(name='foo', testing=True)
        request = get(dwft_foo='1')
        assert waffle.flag_is_active(request, 'foo')
        assert 'foo' in request.waffle_tests
        assert request.waffle_tests['foo']

        request = get(dwft_foo='0')
        assert not waffle.flag_is_active(request, 'foo')
        assert 'foo' in request.waffle_tests
        assert not request.waffle_tests['foo']

    def test_testing_disabled_flag(self):
        Flag.objects.create(name='foo')
        request = get(dwft_foo='1')
        assert not waffle.flag_is_active(request, 'foo')
        assert not hasattr(request, 'waffle_tests')

        request = get(dwft_foo='0')
        assert not waffle.flag_is_active(request, 'foo')
        assert not hasattr(request, 'waffle_tests')


class SwitchTests(TestCase):
    def test_switch_active(self):
        switch = Switch.objects.create(name='myswitch', active=True)
        assert waffle.switch_is_active(switch.name)

    def test_switch_inactive(self):
        switch = Switch.objects.create(name='myswitch', active=False)
        assert not waffle.switch_is_active(switch.name)

    def test_undefined(self):
        assert not waffle.switch_is_active('foo')

    @mock.patch.object(settings._wrapped, 'WAFFLE_SWITCH_DEFAULT', True)
    def test_undefined_default(self):
        assert waffle.switch_is_active('foo')


class SampleTests(TestCase):
    def test_sample_100(self):
        sample = Sample.objects.create(name='sample', percent='100.0')
        assert waffle.sample_is_active(sample.name)

    def test_sample_0(self):
        sample = Sample.objects.create(name='sample', percent='0.0')
        assert not waffle.sample_is_active(sample.name)

    def test_undefined(self):
        assert not waffle.sample_is_active('foo')

    @mock.patch.object(settings._wrapped, 'WAFFLE_SAMPLE_DEFAULT', True)
    def test_undefined_default(self):
        assert waffle.sample_is_active('foo')
