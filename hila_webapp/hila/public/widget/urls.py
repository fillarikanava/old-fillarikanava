from django.conf.urls.defaults import patterns, url
import views

report_id = r'(?P<report_id>\d+)'

urlpatterns = patterns('',
    url('^$', views.front, name='widget_front'),
    url('^map/$', views.map, name='widget_map'),
    url('^latest/$', views.latest, name='widget_single'),
    url('^popular/$', views.popular, name='widget_popular'),
    url('^single/%s/$' % report_id, views.single, name='widget_single'),
)