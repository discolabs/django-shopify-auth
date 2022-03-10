from django.urls import path

from . import views

urlpatterns = [
  path('finalize/',     views.finalize),
  path('authenticate/', views.authenticate),
  path('check-cookie',  views.check_cookie),
  path('',              views.login),
]
