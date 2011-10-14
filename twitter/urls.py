from django.conf.urls.defaults import patterns, include, url

from twap.twitter import views

urlpatterns = patterns('',
    url(r'^tags/$', views.tag_counts, name='tags'),
    url(r'^tags/(?P<filter>\w+)/$', views.tag_counts, name='filtered-tags'),
    url(r'^users/$', views.tweet_counts, name='tweet-counts'),
)
