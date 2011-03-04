from django.http import HttpResponse

from nose.tools import eq_
from test_utils import RequestFactory

from waffle.middleware import WaffleMiddleware


def test_middlware():
    get = RequestFactory().get('/foo')
    get.waffles = {'foo': True, 'bar': False}
    resp = HttpResponse()
    assert not 'dwf_foo' in resp.cookies
    assert not 'dwf_bar' in resp.cookies

    resp = WaffleMiddleware().process_response(get, resp)
    assert 'dwf_foo' in resp.cookies
    assert 'dwf_bar' in resp.cookies

    eq_('True', resp.cookies['dwf_foo'].value)
    eq_('False', resp.cookies['dwf_bar'].value)
