from django.conf.urls.defaults import patterns, url
import views


urlpatterns = patterns('',
    url(r'^xsearch/$', views.xapian_search, name='xap_search_json'),     
    url(r'^timemap/$', views.xapian_search, name='timemap_json_source'),
    url(r'^search2/$', views.search_data_2, name='search_2_json'),     
    url(r'^fileupload/$', views.issue_file_upload, name='upload_issue_files'),
#    url(r'^timemap/$', views.timemap_data, name='timemap_json_source'),
    url(r'^latest/$', views.latest_issue_data, name='latest_json_source'),
    url(r'^addnew/$', views.add_issue, name='add_new_json_reply'),
    url(r'^official/$', views.official_issue_data, name='official_json_source'),
    url(r'^popular/$', views.popular_issue_data, name='popular_json_source'),
    url(r'^ratings/$', views.comment_data, name='comment_json_source'),
    url(r'^vote/$', views.vote_comment, name='comment_vote_json_source'),
    url(r'^issue/$', views.single_issue_data, name='single_issue_json_source'),
    
)
