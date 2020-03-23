from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^finalize/$',     views.finalize),
  url(r'^authenticate/$', views.authenticate),
  url(r'^$',              views.login),
  url(r'^check-cookie$',  views.check_cookie),
]
