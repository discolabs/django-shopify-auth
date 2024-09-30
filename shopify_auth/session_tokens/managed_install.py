import logging
from django.core.exceptions import ImproperlyConfigured

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

from typing import TypedDict


class ResponseData(TypedDict):
    access_token: str
    scope: list[str]


# From https://shopify.dev/docs/apps/build/authentication-authorization/get-access-tokens/exchange-tokens#step-2-get-an-access-token
def retrieve_api_token(shop: str, session_token: str) -> ResponseData:
    url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": settings.SHOPIFY_APP_API_KEY,
        "client_secret": settings.SHOPIFY_APP_API_SECRET,
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "subject_token": session_token,
        "subject_token_type": "urn:ietf:params:oauth:token-type:id_token",
        "requested_token_type": "urn:shopify:params:oauth:token-type:offline-access-token",
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response_data_raw = response.json()
    response_data: ResponseData = {
        "access_token": response_data_raw["access_token"],
        "scope": [scope.strip() for scope in response_data_raw["scope"].split(",")],
    }
    return response_data


def session_token_bounce_page_url(request: HttpRequest) -> str:
    search_params = request.GET.copy()
    search_params.pop("id_token", None)
    search_params["shopify-reload"] = f"{request.path}?{search_params.urlencode()}"
    
    bounce_page_url = settings.SHOPIFY_AUTH_BOUNCE_PAGE_URL
    return f"{bounce_page_url}?{search_params.urlencode()}"


def redirect_to_session_token_bounce_page(request: HttpRequest) -> HttpResponse:
    return redirect(session_token_bounce_page_url(request))
