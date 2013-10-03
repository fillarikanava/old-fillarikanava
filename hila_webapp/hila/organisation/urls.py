from django.conf.urls.defaults import url
from django.contrib.auth.decorators import permission_required
from util.decorators import decorated_patterns
import views

urlpatterns = decorated_patterns('', permission_required('organisation.access'),
    url(r'^filter/save/$', views.filter_save, name='org_filter_save'),
    url(r'^timemap/$', views.timemap, name='org_timemap'),
    url(r'^listview/$', views.listview, name='org_list'),

)