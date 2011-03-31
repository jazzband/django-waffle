from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from test_app import views
from waffle.views import wafflejs


handler404 = None
handler500 = None

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flag_in_view', views.flag_in_view, name='flag_in_view'),
    url(r'^wafflejs$', wafflejs, name='wafflejs'),
    url(r'^switch-on', views.switched_view),
    url(r'^switch-off', views.switched_off_view),
    url(r'^flag-on', views.flagged_view),
    url(r'^flag-off', views.flagged_off_view),
    (r'^admin/', include(admin.site.urls))
)
