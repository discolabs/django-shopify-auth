import shopify

from django.conf import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url

from .decorators import anonymous_required


def get_return_address(request):
    return request.GET.get(auth.REDIRECT_FIELD_NAME) or resolve_url(settings.LOGIN_REDIRECT_URL)


@anonymous_required
def login(request, *args, **kwargs):
    # The `shop` parameter may be passed either directly in query parameters, or
    # as a result of submitting the login form.
    shop = request.POST.get('shop', request.GET.get('shop'))

    # If the shop parameter has already been provided, attempt to authenticate immediately.
    if shop:
        return authenticate(request, *args, **kwargs)

    return render(request, "shopify_auth/login.html", {
        'SHOPIFY_APP_NAME': settings.SHOPIFY_APP_NAME
    })


@anonymous_required
def authenticate(request, *args, **kwargs):
    shop = request.POST.get('shop', request.GET.get('shop'))

    if settings.SHOPIFY_APP_DEV_MODE:
        return finalize(request, token='00000000000000000000000000000000', *args, **kwargs)

    if shop:
        redirect_uri = request.build_absolute_uri(reverse(finalize))
        scope = settings.SHOPIFY_APP_API_SCOPE
        permission_url = shopify.Session(shop.strip()).create_permission_url(scope, redirect_uri)

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


@anonymous_required
def finalize(request, *args, **kwargs):
    shop = request.POST.get('shop', request.GET.get('shop'))

    try:
        shopify_session = shopify.Session(shop, token=kwargs.get('token'))
        shopify_session.request_token(request.GET)
    except:
        login_url = reverse(login)
        return HttpResponseRedirect(login_url)

    # Attempt to authenticate the user and log them in.
    user = auth.authenticate(myshopify_domain=shopify_session.url, token=shopify_session.token)
    if user:
        auth.login(request, user)

    return_address = get_return_address(request)
    return HttpResponseRedirect(return_address)
