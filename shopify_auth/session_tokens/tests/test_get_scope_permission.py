from django.test import Client, TestCase
from django.test.client import RequestFactory

from django.contrib.auth import get_user_model
from shopify_auth.session_tokens.views import get_scope_permission


class GetScopePermissionTest(TestCase):
    def test_get_scope_permission_not_embedded(self):
        self.client = Client()
        rf = RequestFactory()
        self.myshopify_domain = "test-1.myshopify.com"
        shop = get_user_model().objects.create(myshopify_domain=self.myshopify_domain)
        request = rf.get(f"/?shop={shop.myshopify_domain}")
        request.user = shop
        response = get_scope_permission(request, shop.myshopify_domain)
        self.assertRedirects(response, "https://test-1.myshopify.com/admin/oauth/authorize?client_id=test-api-key&redirect_uri=http%3A%2F%2Ftestserver%2Fsession_tokens%2Ffinalize&scope=read_products", fetch_redirect_response=False)


    def test_get_scope_permission_embedded(self):
        self.client = Client()
        rf = RequestFactory()
        self.myshopify_domain = "test-1.myshopify.com"
        shop = get_user_model().objects.create(myshopify_domain=self.myshopify_domain)
        request = rf.get(f"/?shop={shop.myshopify_domain}&embedded=1&host=placeholder")
        request.user = shop
        response = get_scope_permission(request, shop.myshopify_domain)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, shop.myshopify_domain)
