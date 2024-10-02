from django.test import TestCase, RequestFactory
from django.core.exceptions import ImproperlyConfigured
from unittest.mock import patch

from ..managed_install import (
    retrieve_api_token,
    session_token_bounce_page_url,
    redirect_to_session_token_bounce_page,
)

class ManagedInstallTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('requests.post')
    def test_retrieve_api_token(self, mock_post):
        # Mock the response from Shopify
        mock_response = mock_post.return_value
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'scope': 'read_products,write_orders'
        }

        result = retrieve_api_token('test-shop.myshopify.com', 'test_session_token')

        self.assertEqual(result['access_token'], 'test_token')
        self.assertEqual(result['scope'], ['read_products', 'write_orders'])

        # Check if the request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], 'https://test-shop.myshopify.com/admin/oauth/access_token')

    def test_session_token_bounce_page_url(self):
        request = self.factory.get('/test-path/?param1=value1&id_token=test_token')
        
        with self.settings(SHOPIFY_AUTH_BOUNCE_PAGE_URL='/bounce/'):
            url = session_token_bounce_page_url(request)

        expected_url = '/bounce/?param1=value1&shopify-reload=%2Ftest-path%2F%3Fparam1%3Dvalue1'
        self.assertEqual(url, expected_url)

    def test_redirect_to_session_token_bounce_page(self):
        request = self.factory.get('/test-path/')
        
        with self.settings(SHOPIFY_AUTH_BOUNCE_PAGE_URL='/bounce/'):
            response = redirect_to_session_token_bounce_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/bounce/'))
