from django.conf.urls.defaults import *


urlpatterns = patterns('twap.accounts.views',
    url(r'^login/$', 'authenticate_user', name='login'),
    url(r'^logout/$', 'logout_user', name='logout'),
)