from django.conf.urls import patterns, url
from views import LoginView, AuthenticateView, FinalizeView, LogoutView

urlpatterns = patterns('',
  url(r'^authenticate/$', AuthenticateView.as_view(), name = "shopify_authenticate"),
  url(r'^finalize/$',     FinalizeView.as_view(),     name = "shopify_finalize"),
  url(r'^logout/$',       LogoutView.as_view(),       name = "shopify_logout"),
  url(r'^$',              LoginView.as_view(),        name = "shopify_login"),
)