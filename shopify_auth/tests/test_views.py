from django.test import TestCase, Client
from django.conf import settings


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        settings.SHOPIFY_APP_DEV_MODE = False
        self.client = None

    def test_login_view(self):
        """
        Test the login view loads when we're an anonymous user.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_authenticate_view(self):
        """
        Test the authenticate view renders correctly with a shop param.
        """
        response = self.client.get('/authenticate/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/authenticate/', follow=True)
        self.assertEqual(response.status_code, 404)
        response = self.client.post('/authenticate/')
        self.assertEqual(response.status_code, 302)

        # Dev mode so token does not need to be valid
        settings.SHOPIFY_APP_DEV_MODE = True
        response = self.client.get('/authenticate/?shop=test.myshopify.com')
        self.assertEqual(response.status_code, 302)
        self.assertGreater(int(self.client.session['_auth_user_id']), 0)
        self.assertEqual(self.client.session['_auth_user_backend'], 'shopify_auth.backends.ShopUserBackend')
        self.assertIsNot(self.client.session['_auth_user_hash'], None)

    def test_authenticates_standalone_app_with_shop_param(self):
        response = self.client.get('/?shop=test.myshopify.com')
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_view(self):
        """
        Test that return_address is persisted through login flow.
        """
        response = self.client.get('/authenticate/?shop=test.myshopify.com&next=other-view')
        self.assertRedirects(response, 'https://test.myshopify.com/admin/oauth/authorize?client_id=test-api-key&scope=read_products&redirect_uri=http%3A%2F%2Ftestserver%2Ffinalize%2F', fetch_redirect_response=False)

        settings.SHOPIFY_APP_DEV_MODE = True
        response = self.client.get('/authenticate/?shop=test.myshopify.com')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'other-view')
