from django import template
from django.contrib.auth.models import AnonymousUser
from django.template import Template
from django.template.base import VariableNode
from django.test import RequestFactory
from django.test.utils import override_settings
import mock

from test_app import views
from waffle.middleware import WaffleMiddleware
from waffle.tests.base import TestCase


def get():
    request = RequestFactory().get('/foo')
    request.user = AnonymousUser()
    return request


def process_request(request, view):
    response = view(request)
    return WaffleMiddleware().process_response(request, response)


class WaffleTemplateTests(TestCase):

    def test_django_tags(self):
        request = get()
        response = process_request(request, views.flag_in_django)
        self.assertContains(response, 'flag off')
        self.assertContains(response, 'switch off')
        self.assertContains(response, 'sample')
        self.assertContains(response, 'flag_var off')
        self.assertContains(response, 'switch_var off')
        self.assertContains(response, 'sample_var')
        self.assertContains(response, 'window.waffle =')

    def test_get_nodes_by_type(self):
        """WaffleNode.get_nodes_by_type() should correctly find all child nodes"""
        test_template = Template('{% load waffle_tags %}{% switch "x" %}{{ a }}{% else %}{{ b }}{% endswitch %}')
        children = test_template.nodelist.get_nodes_by_type(VariableNode)
        self.assertEqual(len(children), 2)

    def test_no_request_context(self):
        """Switches and Samples shouldn't require a request context."""
        request = get()
        content = process_request(request, views.no_request_context)
        assert 'switch off' in content
        assert 'sample' in content

    @override_settings(TEMPLATE_LOADERS=(
        'jingo.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ))
    @mock.patch.object(template.loader, 'template_source_loaders', None)
    def test_jingo_tags(self):
        """
            We're manually changing default TEMPLATE_LOADERS to enable jingo

            template_source_loaders needs to be patched to None, otherwise
            TEMPLATE_LOADERS won't be overriden.
        """
        request = get()
        response = process_request(request, views.flag_in_jingo)
        self.assertContains(response, 'flag off')
        self.assertContains(response, 'switch off')
        self.assertContains(response, 'sample')
        self.assertContains(response, 'window.waffle =')
