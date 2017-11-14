from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

from shopify_auth.models import AbstractShopUser


class AuthAppShopUser(AbstractShopUser):
    class Meta:
        app_label = 'shopify_auth'


class ViewsTestCase(TestCase):

    def setUp(self):
        settings.AUTH_USER_MODEL = 'shopify_auth.AuthAppShopUser'

    def test_create_super_user(self):
        call_command('createsuperuser', '--noinput',  myshopify_domain='myshop.shopify.com')
