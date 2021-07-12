import logging

from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic.base import View

import shopify

from django.contrib.auth import get_user_model


from shopify_auth.views import get_return_address


def get_scope_permission(request, myshopify_domain):
    redirect_uri = request.build_absolute_uri(reverse("session_tokens:finalize"))
    myshopify_domain = myshopify_domain.strip()
    permission_url = shopify.Session(
        myshopify_domain,
        getattr(settings, "SHOPIFY_APP_API_VERSION", "unstable"),
    ).create_permission_url(settings.SHOPIFY_APP_API_SCOPE, redirect_uri)

    return render(
        request,
        "shopify_auth/iframe_redirect.html",
        {"shop": myshopify_domain, "redirect_uri": permission_url},
    )


class FinalizeAuthView(View):
    def get(self, request):
        myshopify_domain = request.GET.get("shop")
        encoded_host = request.GET.get("host")

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

        return HttpResponseRedirect(
            get_return_address(request) + f"?shop={myshopify_domain}&host={encoded_host}"
        )
