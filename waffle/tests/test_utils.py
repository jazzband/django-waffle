from __future__ import unicode_literals

from django.conf import settings
from django.db.models.base import ModelBase
from django.test import TestCase
from django.test.utils import override_settings

from waffle import defaults
from waffle.utils import get_flag_model, get_setting


class GetSettingTests(TestCase):

    def test_overridden_setting(self):
        prefix = get_setting('CACHE_PREFIX')
        self.assertEqual(settings.WAFFLE['CACHE_PREFIX'], prefix)

    def test_default_setting(self):
        age = get_setting('MAX_AGE')
        self.assertEqual(defaults.MAX_AGE, age)

    def test_override_settings(self):
        assert not get_setting('OVERRIDE')
        with override_settings(WAFFLE={'OVERRIDE': True}):
            assert get_setting('OVERRIDE')

class GetFlagModelTest(TestCase):

    def test_get_flag_model(self):
        flag_model = get_flag_model()
        assert type(flag_model) == ModelBase

    @override_settings(WAFFLE={})
    def test_get_flag_model_fails_when_unset(self):
        with self.assertRaises(AttributeError):
            get_flag_model()

    @override_settings(WAFFLE={'FLAG_CLASS': 'test_app.NoSuchModel'})
    def test_get_flag_model_fails_when_wrong(self):
        with self.assertRaises(LookupError):
            get_flag_model()
