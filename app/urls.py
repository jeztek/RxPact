from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'home'),

    (r'^about/$', 'about'),
    (r'^blog/$', 'blog'),
    (r'^contact/$', 'contact'),

    (r'^/$', 'home'),
)
