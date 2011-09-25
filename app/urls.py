from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'home'),
    (r'^done/', 'done'),
)
