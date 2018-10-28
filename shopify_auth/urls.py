from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^finalize/$',        views.finalize),
  url(r'^authenticate/$',    views.authenticate),
  url(r'^enable_cookies/$',  views.enable_cookies),
  url(r'^$',                 views.login),
]
