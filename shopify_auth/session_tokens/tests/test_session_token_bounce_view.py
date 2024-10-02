from django.test import TestCase, RequestFactory
from django.conf import settings
from django.http import HttpResponse

from ..views import session_token_bounce

class SessionTokenBounceTestCase(TestCase):
    def test_session_token_bounce(self):
        request = RequestFactory().get('/bounce/')
        response = session_token_bounce(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Type'], 'text/html')
        self.assertIn(settings.SHOPIFY_APP_API_KEY, response.content.decode())
        self.assertIn('https://cdn.shopify.com/shopifycloud/app-bridge.js', response.content.decode())