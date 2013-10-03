from django.conf.urls.defaults import patterns, url
from hila import urls

import views

urlpatterns = patterns('',
    url(r'^$', views.front, name='public_front'),
    url(r'^beta', views.betafront, name='public_beta'),
    url(r'^advice$', views.advice, name='public_advice'),
    url(r'^ohjeet$', views.advice, name='public_advice'),
    url(r'^contact$', views.contact, name='public_contact'),
    url(r'^yhteystiedot$', views.contact, name='public_contact'),
    url(r'^feedback$', views.feedback, name='public_feedback'),
    url(r'^palaute$', views.feedback, name='public_feedback'),
    url(r'^info$', views.info, name='public_info'),
    url(r'^media$', views.media, name='public_media'),  
    url(r'^privacy$', views.privacy, name='public_privacy'),  
    url(r'^settings.js$', views.settings, name='public_settings'),
    url(r'^%s/%s/$' % (urls.year, urls.month), views.for_date, name='archives_for_date'),
    url(r'^talvikysely', views.talvikysely, name='public_talvikysely'),
    url(r'^theme/(?P<theme>[a-zA-Z_]+)/$', views.themed, name='public_themed_front'),
)