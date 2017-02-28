from django.test import TestCase, Client


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
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
        response = self.client.get('/?shop=test.myshopify.com')
        self.assertContains(response, 'window.top.location.href = "https://test.myshopify.com/admin/oauth/authorize')
