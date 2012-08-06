from django.conf.urls.defaults import patterns, url

from waffle.views import wafflejs

urlpatterns = patterns('',
    url(r'^wafflejs$', wafflejs, name='wafflejs'),
)
