import logging
import base64
import urllib.parse
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic.base import View

import shopify

from django.contrib.auth import get_user_model


def base64_decode(string):
    """
    Adds back in the required padding before decoding.
    """
    padding = 4 - (len(string) % 4)
    string = string + ("=" * padding)
    return base64.urlsafe_b64decode(string)


def get_scope_permission(request, myshopify_domain):
    redirect_uri = request.build_absolute_uri(reverse("session_tokens:finalize"))
    myshopify_domain = myshopify_domain.strip()
    permission_url = shopify.Session(
        myshopify_domain,
        getattr(settings, "SHOPIFY_APP_API_VERSION", "unstable"),
    ).create_permission_url(settings.SHOPIFY_APP_API_SCOPE, redirect_uri)

    embedded = request.GET.get("embedded")
    if not embedded or embedded != "1":
        return HttpResponseRedirect(permission_url)

    host = request.GET.get("host")
    if not host:
        raise Exception("expected host query parameter when embedded=1 is present")

    return render(
        request,
        "shopify_auth/iframe_redirect.html",
        {"host": host, "redirect_uri": permission_url},
    )


class FinalizeAuthView(View):
    def get(self, request):
        myshopify_domain = request.GET.get("shop")

        try:
            shopify_session = shopify.Session(
                myshopify_domain,
                getattr(settings, "SHOPIFY_APP_API_VERSION", "unstable"),
            )
            shopify_session.request_token(request.GET)
        except:
            logging.exception("Shopify login failed.")
            return HttpResponse("Shopify login failed.")

        shop = get_user_model().update_or_create(shopify_session, request)
        shop.install(request)

        if host := request.GET.get("host"):
            decoded_host = base64_decode(host).decode('utf-8')
            redirect_url = f"https://{decoded_host}/apps/{settings.SHOPIFY_APP_API_KEY}"
            return HttpResponseRedirect(redirect_url)


        return HttpResponseRedirect(
            f"https://{myshopify_domain}/admin/apps/{settings.SHOPIFY_APP_API_KEY}"
        )


def session_token_bounce(request) -> HttpResponse:
    """
    The entire flow is documented on https://shopify.dev/docs/apps/build/authentication-authorization/set-embedded-app-authorization?extension=javascript#session-token-in-the-url-parameter
    """
    response = HttpResponse(content_type="text/html")
    html = f"""
    <head>
        <meta name="shopify-api-key" content="{settings.SHOPIFY_APP_API_KEY}" />
        <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
    </head>
    """
    response.write(html)
    return response
