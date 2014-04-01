from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^finalize/$',     'shopify_auth.views.finalize'),
    url(r'^authenticate/$', 'shopify_auth.views.authenticate'),
    url(r'^$',              'shopify_auth.views.login'),
)