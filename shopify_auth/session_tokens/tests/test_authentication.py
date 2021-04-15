from django.test import RequestFactory, TestCase
import jwt
from django.conf import settings
from ..middleware import authenticate
from django.contrib.auth import get_user_model


def generate_jwt_token(shop):
    return jwt.encode(
        {
            "iss": f"https://{shop.myshopify_domain}",
            "dest": f"https://{shop.myshopify_domain}",
        },
        settings.SHOPIFY_APP_API_SECRET,
    )


class ShopifyTokenAuthenticationTest(TestCase):
    def setUp(self):
        settings.AUTH_USER_MODEL = "shopify_auth.AuthAppShopUser"
        self.myshopify_domain = "test-1.myshopify.com"
        self.user = get_user_model().objects.create(
            myshopify_domain=self.myshopify_domain
        )
        self.factory = RequestFactory()
        self.valid_token = f"Bearer {generate_jwt_token(self.user)}"

    def test_valid_token(self):
        request = self.factory.get("/", HTTP_AUTHORIZATION=self.valid_token)
        user = authenticate(request)
        self.assertEqual(user.myshopify_domain, self.myshopify_domain)
        self.assertEqual(self.user.id, user.id)

    def test_not_existing_app_installation_valid_token(self):
        self.user.delete()
        request = self.factory.get("/", HTTP_AUTHORIZATION=self.valid_token)
        user = authenticate(request)
        self.assertIsNone(user)

    def test_invalid_token(self):
        jwt_token = "Bearer not_jwt"
        request = self.factory.get("/", HTTP_AUTHORIZATION=jwt_token)
        user = authenticate(request)
        self.assertIsNone(user)

    def test_missing_header(self):
        request = self.factory.get("/")
        result = authenticate(request)
        self.assertIsNone(result)

    def test_empty_header(self):
        request = self.factory.get("/", HTTP_AUTHORIZATION="")
        result = authenticate(request)
        self.assertIsNone(result)
