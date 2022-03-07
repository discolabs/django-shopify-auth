from django.urls import re_path

from . import views

urlpatterns = [
  path('finalize/',     views.finalize),
  path('authenticate/', views.authenticate),
  path('',              views.login),
  path('check-cookie',  views.check_cookie),
]
