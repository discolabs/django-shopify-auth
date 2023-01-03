from unittest.mock import patch

from django.shortcuts import reverse
from shopify_auth.tests.test_user import ViewsTestCase

from django.contrib.auth import get_user_model
import shopify

HOST_MYSHOPIFY_DOMAIN = "cmFuZG9tX3Nob3AubXlzaG9waWZ5LmNvbS9hZG1pbg"
HOST_ADMIN_SHOPIFY_COM = "YWRtaW4uc2hvcGlmeS5jb20vc3RvcmUvam9zZWYtZGV2LTIwMjEtMDc"

def request_token(self, params):
    self.token = "TOKEN"


class FinalizeViewTest(ViewsTestCase):
    def setUp(self):
        super().setUp()
        self.shop_patcher = patch("shopify.Shop", autospec=True)
        mck = self.shop_patcher.start()
        mck.current().currency = "CZK"
        self.addCleanup(self.shop_patcher.stop)
        self.url = reverse("session_tokens:finalize") + "?shop=random_shop.myshopify.com"

    @patch.object(shopify.Session, "request_token", request_token)
    def test_creates_user(self):
        response = self.client.get(self.url)
        AuthAppShopUser = get_user_model()
        self.assertTrue(
            AuthAppShopUser.objects.filter(
                myshopify_domain="random_shop.myshopify.com"
            ).exists()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://random_shop.myshopify.com/admin/apps/test-api-key")


    @patch.object(shopify.Session, "request_token", request_token)
    def test_creates_user_redirects_host_myshopify(self):
        response = self.client.get(f"{self.url}&host={HOST_MYSHOPIFY_DOMAIN}")
        AuthAppShopUser = get_user_model()
        self.assertTrue(
            AuthAppShopUser.objects.filter(
                myshopify_domain="random_shop.myshopify.com"
            ).exists()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://random_shop.myshopify.com/admin/apps/test-api-key")


    @patch.object(shopify.Session, "request_token", request_token)
    def test_creates_user_redirects_host_admin_shopify_com(self):
        response = self.client.get(f"{self.url}&host={HOST_ADMIN_SHOPIFY_COM}")
        AuthAppShopUser = get_user_model()
        self.assertTrue(
            AuthAppShopUser.objects.filter(
                myshopify_domain="random_shop.myshopify.com"
            ).exists()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://admin.shopify.com/store/josef-dev-2021-07/apps/test-api-key")
