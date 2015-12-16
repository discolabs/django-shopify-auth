from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import shopify


class ShopifyAuthConfig(AppConfig):
    """
    Application configuration for the Shopify Auth application.
    """

    name = 'shopify_auth'
    verbose_name = 'Shopify Auth'

    def ready(self):
        """
        The ready() method is called after Django setup.
        """
        initialise_shopify_session()


def initialise_shopify_session():
    """
    Initialise the Shopify session with the Shopify App's API credentials.
    """
    if not settings.SHOPIFY_APP_API_KEY or not settings.SHOPIFY_APP_API_SECRET:
        raise ImproperlyConfigured("SHOPIFY_APP_API_KEY and SHOPIFY_APP_API_SECRET must be set in settings")
    shopify.Session.setup(api_key=settings.SHOPIFY_APP_API_KEY, secret=settings.SHOPIFY_APP_API_SECRET)
