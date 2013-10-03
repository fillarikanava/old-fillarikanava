from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns('',
    url(r'^timemap/$', views.timemap, name='browse_timemap'),
)