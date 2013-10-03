from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin
from django.template import add_to_builtins
from django.views.decorators.cache import never_cache
from util.decorators import decorated_patterns

from hila.feeds.latest import latest as latestfeed, latest_messages, latest_comments

year, month = r'(?P<year>\d{4})', r'(?P<month>\d{1,2})'

add_to_builtins('django.templatetags.i18n')
add_to_builtins('hila.templatetags.filters')
#add_to_builtins('hila.templatetags.map_search_filter')

handler500, handler404 = 'views.handler500', 'views.handler404'

feeds = {
    'latest': latestfeed,
    'latest_messages' : latest_messages,
    'latest_comments' : latest_comments,
    }



from hila.admin.site import admin

#admin.autodiscover()


urlpatterns = patterns( settings.DJANGO_URL_PREFIX,
    (r'^a/', include('hila.public.archives.urls')),
    (r'^accounts/', include('hila.public.signup.urls')),
    (r'^fbconnect/', include('hila.facebookconnect.urls')),
    (r'^user/', include('hila.public.profiles.urls')),
    (r'^api/', include('hila.api.urls')),
    (r'^b/', include('hila.public.browse.urls')),
    (r'^o/', include('hila.organisation.urls')),
    (r'^r/', include('hila.public.report.urls')),
    ('^widget/', include('hila.public.widget.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('hila.public.front.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)


if settings.DEBUG:
#    admin.autodiscover()
    urlpatterns = patterns('',
#        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#        (r'^admin/(.*)', admin.site.root),
    ) + decorated_patterns('', never_cache,
        (r'^%s(?P<path>.+)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns

