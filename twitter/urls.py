from django.conf.urls.defaults import patterns, include, url

from twap.twitter import views

urlpatterns = patterns('twap.twitter.views',
    url(r'^$', 'summary', name='summary'),
    url(r'^hashtags/$', 'tag_list', name='tag_list'),
    url(r'^hashtags/(?P<tag_slug>\w+)/$', 'tag_view', name='tag_view'),
    url(r'^users/$', 'user_list', name='user_list'),
    url(r'^users/(?P<screen_name>\w+)/$', 'user_view', name='user_view'),
)
