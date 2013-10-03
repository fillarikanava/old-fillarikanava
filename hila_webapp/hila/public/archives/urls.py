from django.conf.urls.defaults import patterns, url
from hila import urls
import views

urlpatterns = patterns('',
    url(r'^$', views.status_index, name='archives_index_status'),
    url(r'^date/$', views.date_index, name='archives_index_date'),
    url(r'^search/$', views.search, name='archives_search'),
    url(r'^%s/%s/$' % (urls.year, urls.month), views.for_date, name='archives_for_date'),
#    url(r'^(?<year>\d{2})/(?<month>\d{1,2})/$', views.by_date, name='archives_by_date'),
#    url(r'^(?<status>\w+)/$', views.by_status, name='archives_by_status'),
)