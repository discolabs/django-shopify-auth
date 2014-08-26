VERSION     = (0, 1, 7)
__version__ = '.'.join(map(str, VERSION))
__author__  = 'Gavin Ballard'


def initialize():
    """
    Initialise the Shopify session with the App's credentials. The import statements are inside the function to
    prevent issues when installing this package (as the __init__.py file is read during setup).
    For Django 1.7, this will be handled by the app configuration.
    """
    import shopify

    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured

    if not settings.SHOPIFY_APP_API_KEY or not settings.SHOPIFY_APP_API_SECRET:
        raise ImproperlyConfigured("SHOPIFY_APP_API_KEY and SHOPIFY_APP_API_SECRET must be set in settings")
    shopify.Session.setup(api_key = settings.SHOPIFY_APP_API_KEY, secret = settings.SHOPIFY_APP_API_SECRET)