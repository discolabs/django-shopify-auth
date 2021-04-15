from unittest.mock import patch

from django.shortcuts import reverse
from shopify_auth.tests.test_user import ViewsTestCase

from django.contrib.auth import get_user_model
import shopify


def request_token(self, params):
    self.token = "TOKEN"


class FinalizeViewTest(ViewsTestCase):
    def setUp(self):
        super().setUp()
        self.shop_patcher = patch("shopify.Shop", autospec=True)
        mck = self.shop_patcher.start()
        mck.current().currency = "CZK"
        self.addCleanup(self.shop_patcher.stop)
        self.url = reverse("session_tokens:finalize") + "?shop=random_shop"

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
