from django.shortcuts import reverse
from django.test import Client, TestCase
from django.test.client import RequestFactory

from shopify_auth.shopify_auth.views import get_scope_permission


class GetScopePermissionTest(TestCase):
    def test_get_scope_permission(self):
        self.client = Client()
        rf = RequestFactory()
        shop = AuthAppShopUserFactory()
        request = rf.get(reverse("console:dashboard") + f"?{shop.myshopify_domain}")
        request.user = shop
        response = get_scope_permission(request, shop.myshopify_domain)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, shop.myshopify_domain)
