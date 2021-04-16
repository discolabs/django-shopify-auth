import logging
from urllib.parse import urlparse

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from django.conf import settings
from django.contrib.auth import get_user_model

INVALID_TOKEN_MESSAGE = "Invalid JWT Token"


class ShopifyTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"

    @staticmethod
    def get_hostname(url):
        return urlparse(url).netloc

    def authenticate(self, request):
        UserModel = get_user_model()
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        if len(auth) == 1:
            msg = "Invalid token header. No credentials provided."
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid token header. Token string should not contain spaces."
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = "Invalid token header. Token string should not contain invalid characters."
            raise AuthenticationFailed(msg)

        try:
            decoded_payload = jwt.decode(
                token,
                settings.SHOPIFY_APP_API_SECRET,
                algorithms=["HS256"],
                audience=settings.SHOPIFY_APP_API_KEY,
                options={"verify_sub": False, "verify_nbf": False},
            )
            dest_host = self.get_hostname(decoded_payload["dest"])
            iss_host = self.get_hostname(decoded_payload["iss"])
            if dest_host != iss_host:
                raise AuthenticationFailed(INVALID_TOKEN_MESSAGE)

            try:
                return UserModel.objects.get(myshopify_domain=dest_host), token
            except UserModel.DoesNotExist:
                raise AuthenticationFailed(INVALID_TOKEN_MESSAGE)

        except (ExpiredSignatureError, JWTError, JWTClaimsError) as e:
            logging.warning(f"Login user failed: {e}.")
            raise AuthenticationFailed(INVALID_TOKEN_MESSAGE)
