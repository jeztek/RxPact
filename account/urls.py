from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('account.views',
    (r'^$', 'settings'),

    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
)
