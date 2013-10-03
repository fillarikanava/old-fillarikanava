from django.conf.urls.defaults import *

from hila.public.profiles import views


urlpatterns = patterns('',
                       url(r'^create/$',
                           views.create_profile,
                           name='profiles_create_profile'),
                       url(r'^edit/$',
                           views.edit_profile,
                           name='profiles_edit_profile'),
                        url(r'^anonymous/$',
                           views.anonymous_detail,
                           name='anonymous_profile'),
                       url(r'^(?P<username>\w+)/$',
                           views.profile_detail,
                           name='user_profile'),
                       url(r'^$',
                           views.profile_list,
                           name='profiles_profile_list'),
                       )
