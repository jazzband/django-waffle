from __future__ import unicode_literals

from django.conf.urls import patterns, url

from waffle.views import wafflejs

urlpatterns = patterns('',
    url(r'^wafflejs$', wafflejs, name='wafflejs'),
)
