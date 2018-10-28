import shopify

from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url

from .decorators import anonymous_required

if DJANGO_VERSION >= (2, 0, 0):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

def get_return_address(request):
    return request.GET.get(auth.REDIRECT_FIELD_NAME) or resolve_url(settings.LOGIN_REDIRECT_URL)

def authenticate_at_top_level(request, shop):
    request.session['shopify.top_level_oauth'] = True
    return render(request, 'shopify_auth/iframe_redirect.html', {
        'shop': shop,
        'redirect_uri': request.build_absolute_uri(reverse(authenticate) + '?shop=' + shop)
    })

def request_cookies(request, shop):
    request.session['shopify.cookies_persist'] = True
    return render(request, 'shopify_auth/iframe_redirect.html', {
        'shop': shop,
        'redirect_uri': request.build_absolute_uri(reverse(enable_cookies) + '?shop=' + shop)
    })

@anonymous_required
def login(request, *args, **kwargs):
    # The `shop` parameter may be passed either directly in query parameters, or
    # as a result of submitting the login form.
    shop = request.POST.get('shop', request.GET.get('shop'))

    if not shop:
        return render(request, 'shopify_auth/login.html', {
            'SHOPIFY_APP_NAME': settings.SHOPIFY_APP_NAME
        })

    # If the shop parameter has already been provided, attempt to authenticate immediately.

    if request.session.get('shopify.cookies_persist'):
        if request.session.get('shopify.top_level_oauth'):
            return authenticate(request, *args, **kwargs)
        else:
            return authenticate_at_top_level(request, shop)
    else:
        return request_cookies(request, shop)


@anonymous_required
def authenticate(request, *args, **kwargs):
    shop = request.POST.get('shop', request.GET.get('shop'))

    if settings.SHOPIFY_APP_DEV_MODE:
        return finalize(request, token='00000000000000000000000000000000', *args, **kwargs)

    if shop:
        redirect_uri = request.build_absolute_uri(reverse(finalize))
        scope = settings.SHOPIFY_APP_API_SCOPE
        permission_url = shopify.Session(shop.strip()).create_permission_url(scope, redirect_uri)

        if settings.SHOPIFY_APP_IS_EMBEDDED and not request.session.get('shopify.top_level_oauth'):
            # Embedded Apps should use a Javascript redirect. With exception when handling ITP 2.0 protection.
            return render(request, 'shopify_auth/iframe_redirect.html', {
                'shop': shop,
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
        del request.session['shopify.top_level_oauth']
    except KeyError:
        pass

    try:
        shopify_session = shopify.Session(shop, token=kwargs.get('token'))
        shopify_session.request_token(request.GET)
    except:
        login_url = reverse(login)
        return HttpResponseRedirect(login_url)

    # Attempt to authenticate the user and log them in.
    user = auth.authenticate(request=request, myshopify_domain=shopify_session.url, token=shopify_session.token)
    if user:
        auth.login(request, user)

    return_address = get_return_address(request)
    return HttpResponseRedirect(return_address)

def enable_cookies(request, *args, **kwargs):
    shop = request.POST.get('shop', request.GET.get('shop'))
    return render(request, 'shopify_auth/enable_cookies.html', {
        'shop': shop,
    })
