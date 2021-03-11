from django.test import RequestFactory, TestCase
from rest_framework.exceptions import AuthenticationFailed

from console.factories import AppInstallationFactory, generate_jwt_token
from shopify_auth.authentication import ShopifyTokenAuthentication
from upsell_platform.shopify_apps import ShopifyApp


class ShopifyTokenAuthenticationTest(TestCase):
    def setUp(self):
        self.myshopify_domain = "test-1.myshopify.com"
        self.factory = RequestFactory()
        self.authentication = ShopifyTokenAuthentication()
        self.shopify_app = ShopifyApp.get("candyrack")
        self.app_install = AppInstallationFactory(
            shop__myshopify_domain=self.myshopify_domain, app_id=self.shopify_app.id
        )
        self.valid_token = f"Bearer {generate_jwt_token(self.app_install)}"
        ShopifyApp.configure()

    def test_valid_token(self):
        request = self.factory.get("/", HTTP_AUTHORIZATION=self.valid_token)
        request.shopify_app = self.shopify_app
        user, app_install = self.authentication.authenticate(request)
        self.assertEqual(user.myshopify_domain, self.myshopify_domain)
        self.assertEqual(app_install.shop_id, user.id)

    def test_not_existing_app_installation_valid_token(self):
        self.app_install.delete()
        request = self.factory.get("/", HTTP_AUTHORIZATION=self.valid_token)
        request.shopify_app = self.shopify_app
        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(request)

    def test_inactive_app_installation_valid_token(self):
        self.app_install.uninstall()
        request = self.factory.get("/", HTTP_AUTHORIZATION=self.valid_token)
        request.shopify_app = self.shopify_app
        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(request)

    def test_invalid_token(self):
        jwt_token = "Bearer not_jwt"
        request = self.factory.get("/", HTTP_AUTHORIZATION=jwt_token)
        request.shopify_app = self.shopify_app
        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate(request)

    def test_missing_header(self):
        request = self.factory.get("/")
        request.shopify_app = self.shopify_app
        result = self.authentication.authenticate(request)
        self.assertIsNone(result)

    def test_empty_header(self):
        request = self.factory.get("/", HTTP_AUTHORIZATION="")
        request.shopify_app = self.shopify_app
        result = self.authentication.authenticate(request)
        self.assertIsNone(result)
