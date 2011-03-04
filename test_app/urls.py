from django.conf.urls.defaults import patterns, url

from test_app import views


handler404 = None
handler500 = None


urlpatterns = patterns('',
    url(r'^flag_in_view', views.flag_in_view, name='flag_in_view'),
)
