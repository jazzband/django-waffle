from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.http import HttpResponseNotFound, HttpResponseServerError

from test_app import views


handler404 = lambda r: HttpResponseNotFound()
handler500 = lambda r: HttpResponseServerError()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flag_in_view', views.flag_in_view, name='flag_in_view'),
    url(r'^switch-on', views.switched_view),
    url(r'^switch-off', views.switched_off_view),
    url(r'^flag-on', views.flagged_view),
    url(r'^flag-off', views.flagged_off_view),
    (r'^', include('waffle.urls')),
    (r'^admin/', include(admin.site.urls))
)
