from django.conf.urls.defaults import patterns, include, url

from twap.twitter import views

urlpatterns = patterns('twap.twitter.views',
    url(r'^$', 'summary', name='summary'),
    url(r'^hashtags/$', 'tag_counts', name='tags'),
    url(r'^hashtags/(?P<filter>\w+)/$', 'tag_counts', name='filtered-tags'),
    url(r'^users/$', 'tweet_counts_by_user', name='tweet-counts'),
)
