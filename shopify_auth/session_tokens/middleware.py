import logging
import re
from urllib.parse import urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from django.conf import settings
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError


def get_hostname(url):
    return urlparse(url).netloc


def authenticate(request):
    jwt_token = request.headers.get("Authorization")

    if not jwt_token:
        return

    striped_jwt_token = re.sub(r"Bearer\s", "", jwt_token)
    try:
        decoded_payload = jwt.decode(
            striped_jwt_token,
            settings.SHOPIFY_APP_API_SECRET,
            algorithms=["HS256"],
            audience=settings.SHOPIFY_APP_API_KEY,
            options={"verify_sub": False, "verify_nbf": False},
        )

        dest_host = get_hostname(decoded_payload["dest"])
        iss_host = get_hostname(decoded_payload["iss"])

        assert dest_host == iss_host, "'dest' claim host does not match 'iss' claim host"
        assert dest_host, "'dest' claim host not a valid shopify host"

        return get_user_model().objects.get(myshopify_domain=dest_host)

    except (ExpiredSignatureError, JWTError, JWTClaimsError, AssertionError, ObjectDoesNotExist) as e:
        logging.warning(f"Login user failed: {e}.")

class CookielessAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = authenticate(request)
        if user:
            request.user = user
        return self.get_response(request)

