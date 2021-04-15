from django.test import Client, TestCase
from django.test.client import RequestFactory

from django.contrib.auth import get_user_model
from shopify_auth.session_tokens.views import get_scope_permission


class GetScopePermissionTest(TestCase):
    def test_get_scope_permission(self):
        self.client = Client()
        rf = RequestFactory()
        self.myshopify_domain = "test-1.myshopify.com"
        shop = get_user_model().objects.create(myshopify_domain=self.myshopify_domain)
        request = rf.get(f"/?shop={shop.myshopify_domain}")
        request.user = shop
        response = get_scope_permission(request, shop.myshopify_domain)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, shop.myshopify_domain)
