import logging
import re
from urllib.parse import urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, MissingRequiredClaimError, PyJWTError


def get_hostname(url):
    return urlparse(url).netloc

def decode_token(token):
    decoded_payload = jwt.decode(
        token,
        settings.SHOPIFY_APP_API_SECRET,
        algorithms=["HS256"],
        audience=settings.SHOPIFY_APP_API_KEY,
        options={"verify_sub": False, "verify_nbf": False},
    )
    dest_host = get_hostname(decoded_payload["dest"])
    iss_host = get_hostname(decoded_payload["iss"])

    assert (
        dest_host == iss_host
    ), "'dest' claim host does not match 'iss' claim host"
    assert dest_host, "'dest' claim host not a valid shopify host"

    return dest_host

def get_user(token):
    try:
        dest_host = decode_token(token)
        return get_user_model().objects.get(myshopify_domain=dest_host)

    except (
        ExpiredSignatureError,
        PyJWTError,
        MissingRequiredClaimError,
        AssertionError,
        ObjectDoesNotExist,
        KeyError,
    ) as e:
        logging.warning(f"Login user failed: {e}.")

def authenticate(request):
    jwt_token = request.headers.get("Authorization")

    if not jwt_token:
        return

    striped_jwt_token = re.sub(r"Bearer\s", "", jwt_token)
    return get_user(striped_jwt_token)


class SessionTokensAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = authenticate(request)
        if user:
            request.user = user
        return self.get_response(request)
