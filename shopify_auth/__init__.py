import shopify

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


VERSION     = (0, 1, 2)
__version__ = '.'.join(map(str, VERSION))
__author__  = 'Gavin Ballard'


def initialize():
    if not settings.SHOPIFY_APP_API_KEY or not settings.SHOPIFY_APP_API_SECRET:
        raise ImproperlyConfigured("SHOPIFY_APP_API_KEY and SHOPIFY_APP_API_SECRET must be set in settings")
    shopify.Session.setup(api_key = settings.SHOPIFY_APP_API_KEY, secret = settings.SHOPIFY_APP_API_SECRET)