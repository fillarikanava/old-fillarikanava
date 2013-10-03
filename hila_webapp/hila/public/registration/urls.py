'''
Created on 31.3.2009

@author: jsa
'''

from django.conf.urls.defaults import patterns, url
from django.contrib.auth import urls as auth_urls
from django.views.generic.simple import direct_to_template
import views
from views import xd_receiver, fb_connect, logout_view

urlpatterns = auth_urls.urlpatterns + patterns('',
    url(r'^profile/$', views.profile, name='user_profile'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/complete/$', direct_to_template, {'template':'registration_complete.html'}, name='signup_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', views.activate, name='activate'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^xd_receiver\.htm$', xd_receiver),
    url(r'^fb_connect/$', fb_connect),
    url(r'^profile/$', views.profile, name='user_profiles'),
)