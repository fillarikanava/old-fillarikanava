from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='report_index'),
    url(r'^search/$', views.search, name='report_search'),
    url(r'^create/$', views.create, name='report_create'),
    url(r'^create/(?P<tag>[a-zA-Z_]+)/$', views.create, name='tagged_report_create'),
   # url(r'^create/thanks/$', views.thanks, name='report_thanks'),
    url(r'^(?P<report_id>\d+)/$', views.view, name='report_view'),
    url(r'^(?P<report_id>\d+)/edit/$', views.edit, name='report_edit'),
    url(r'^(?P<report_id>\d+)/delete/$', views.delete, name='report_delete'),
    url(r'^(?P<report_id>\d+)/comment/$', views.comment, name='comment_report'),
    url(r'^(?P<report_id>\d+)/comment/(?P<comment_id>\d+)/edit/$', views.comment_edit, name='comment_report_edit'),
    url(r'^(?P<tag>[a-zA-Z_]+)/(?P<report_id>\d+)/$', views.view, name='tagged_report_view'),
    url(r'^(?P<tag>[a-zA-Z_]+)/(?P<report_id>\d+)/edit/$', views.edit, name='tagged_report_edit'),
    url(r'^(?P<tag>[a-zA-Z_]+)/(?P<report_id>\d+)/delete/$', views.delete, name='tagged_report_delete'),
    url(r'^(?P<tag>[a-zA-Z_]+)/(?P<report_id>\d+)/comment/$', views.comment, name='tagged_comment_report'),
    url(r'^(?P<tag>[a-zA-Z_]+)/(?P<report_id>\d+)/comment/(?P<comment_id>\d+)/edit/$', views.comment_edit, name='tagged_comment_report_edit'),
    url(r'^(?P<tag>[a-zA-Z_]+)/(?P<report_id>\d+)/$', views.view, name='tagged_report_view'),
)