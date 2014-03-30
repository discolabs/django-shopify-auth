from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
import shopify

def get_return_address(request):
  return request.session.get('return_to') or '/'

def login(request, *args, **kwargs):
  shop = request.REQUEST.get('shop')

  # If the shop parameter has already been provided, attempt to authenticate immediately.
  if shop:
    return authenticate(request, *args, **kwargs)

  return render(request, "shopify_auth/login.html")

def authenticate(request, *args, **kwargs):
  shop = request.REQUEST.get('shop')

  if settings.SHOPIFY_APP_DEV_MODE:
    return finalize(request, shopify_session_token = '00000000000000000000000000000000', *args, **kwargs)

  if shop:
    redirect_uri = request.build_absolute_uri(reverse('shopify_auth.views.finalize'))
    shopify_session = shopify.Session(shop)
    scope = settings.SHOPIFY_APP_API_SCOPE
    permission_url = shopify_session.create_permission_url(scope, redirect_uri)

    if settings.SHOPIFY_APP_IS_EMBEDDED:
      # Embedded Apps should use a Javascript redirect.
      return render(request, "shopify_auth/iframe_redirect.html", {
        'redirect_uri': permission_url
      })
    else:
      # Non-Embedded Apps should use a standard redirect.
      return HttpResponseRedirect(permission_url)

  return_address = get_return_address(request)
  return HttpResponseRedirect(return_address)

def finalize(request, *args, **kwargs):
  shop = request.REQUEST.get('shop')

  try:
    shopify_session = shopify.Session(shop, kwargs.get('shopify_session_token'))
    shopify_session.request_token(request.REQUEST)
  except:
    login_url = reverse('shopify_auth.views.login')
    return HttpResponseRedirect(login_url)

  request.session['shopify'] = {
    "shop_url":     shop,
    "access_token": shopify_session.token
  }
  request.session.pop('return_to', None)

  return_address = get_return_address(request)
  return HttpResponseRedirect(return_address)