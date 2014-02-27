from django.views.generic import View, TemplateView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
import shopify

def get_return_address(request):
  return request.session.get('return_to') or '/'

class LoginView(TemplateView):
  template_name = "shopify_auth/login.html"

  def get(self, request, *args, **kwargs):
    """
    Present a form requesting the subdomain of the shop.
    If a shop is already provided, pass along to the authentication view.
    """
    if request.GET.get('shop'):
      authenticate_uri = request.build_absolute_uri(reverse('shopify_authenticate') + '?' + request.GET.urlencode())
      return HttpResponseRedirect(authenticate_uri)

    return super(LoginView, self).get(request, *args, **kwargs)

class AuthenticateView(TemplateView):
  template_name = "shopify_auth/iframe_redirect.html"

  def post(self, request, *args, **kwargs):
    """

    """
    shop = request.POST.get('shop')
    if shop:
      # Embedded apps should redirect using the <iframe> method.
      if settings.SHOPIFY_APP_EMBEDDED:
        redirect_uri = '/auth/shopify?shop=#%s' % shop
        print redirect_uri
        return self.render_to_response({'redirect_uri': redirect_uri})

      # Non-embedded apps should redirect using a standard HTTP redirect.
      shopify_session = shopify.Session(shop)
      scope = settings.SHOPIFY_API_SCOPE
      redirect_uri = request.build_absolute_uri(reverse('shopify_finalize'))
      permission_url = shopify_session.create_permission_url(scope, redirect_uri)
      return HttpResponseRedirect(permission_url)

    return_address = get_return_address(request)
    return HttpResponseRedirect(return_address)

class FinalizeView(View):
  def get(self, request, *args, **kwargs):
    """

    """
    shop = request.REQUEST.get('shop')
    try:
      shopify_session = shopify.Session(shop)
      shopify_session.request_token(request.REQUEST)
    except:
      messages.error(request, "Could not log in to Shopify store.")
      login_url = reverse('shopify_login')
      return HttpResponseRedirect(login_url)

    request.session['shopify'] = {
      "shop_url":     shop,
      "access_token": shopify_session.token
    }
    messages.info(request, "Logged in to shopify store.")
    request.session.pop('return_to', None)

    return_address = get_return_address(request)
    return HttpResponseRedirect(return_address)

class LogoutView(View):
  def get(self, request, *args, **kwargs):
    """

    """
    request.session.pop('shopify', None)
    messages.info(request, "Successfully logged out.")
    login_url = reverse('shopify_login')
    return HttpResponseRedirect(login_url)